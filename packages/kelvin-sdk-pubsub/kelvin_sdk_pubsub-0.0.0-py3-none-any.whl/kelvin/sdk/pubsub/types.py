"""Types."""

import re
from datetime import datetime, timedelta
from ssl import SSLContext
from typing import Any, Optional, Union, cast
from urllib.parse import unquote

from asyncio_mqtt import Client as AsyncClient
from paho.mqtt.client import Client
from pydantic import AnyUrl, BaseConfig, StrictStr, UrlSchemeError
from pydantic.main import ModelField

# basic identifier
BASE_IDENTIFIER = "[{head}]([{mid}]?[{tail}])*"

IDENTIFIER = BASE_IDENTIFIER.format(head="a-zA-Z", mid="_", tail="a-zA-Z0-9")
DNS_NAME = BASE_IDENTIFIER.format(head="a-z", mid="-", tail="a-z0-9")
DOTTED_NAME = rf"{BASE_IDENTIFIER}(\.{BASE_IDENTIFIER})*".format(
    head="a-z",
    mid="-_",
    tail="a-z0-9",
)

TimeType = Union[int, float, datetime, timedelta]


class Identifier(StrictStr):
    """Dotted-identifier name."""

    regex = re.compile(f"^{IDENTIFIER}$")


class DNSName(StrictStr):
    """DNS-safe name."""

    regex = re.compile(f"^{DNS_NAME}$")


class DottedName(StrictStr):
    """Dotted-identifier name."""

    regex = re.compile(f"^{DOTTED_NAME}$")


class MQTTUrl(AnyUrl):
    """MQTT URL."""

    allowed_schemes = {"mqtt", "mqtts"}

    _DEFAULT_PORTS = {"mqtt": "1883", "mqtts": "8883"}

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> AnyUrl:
        """Validate URL."""

        try:
            result = super().validate(value, field, config)
        except UrlSchemeError:
            if not isinstance(value, str):
                raise
            result = super().validate(f"mqtt://{value}", field, config)

        if result.port is None:
            result.port = cls._DEFAULT_PORTS[result.scheme]

        return result

    def get_sync_client(self, client_id: Optional[str] = None) -> Client:
        """Get synchronous client."""

        client = Client(client_id or "")

        if self.user and self.password:
            client.username_pw_set(unquote(self.user), unquote(self.password))

        if self.scheme == "mqtts":
            client.tls_set_context()

        client.connect(self.host, int(cast(int, self.port)))

        return client

    def get_async_client(self, client_id: Optional[str] = None) -> AsyncClient:
        """Get asynchronous client."""

        return AsyncClient(
            self.host,
            int(cast(int, self.port)),
            username=self.user,
            password=self.password,
            client_id=client_id,
            tls_context=SSLContext() if self.scheme == "mqtts" else None,
        )

"""Kelvin Pub-Sub Client Configuration."""

from __future__ import annotations

from collections import defaultdict
from enum import IntEnum
from itertools import product
from pathlib import Path
from typing import (
    Any,
    Callable,
    Collection,
    DefaultDict,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    cast,
)
from urllib.parse import quote, urlunsplit

import yaml
from pydantic import BaseConfig, BaseSettings, Field, ValidationError, root_validator, validator
from pydantic.main import ErrorWrapper, ModelField

from kelvin.icd import Model

from .types import DNSName, DottedName, Identifier, MQTTUrl
from .utils import deep_get

try:
    from functools import cached_property  # type: ignore
except ImportError:  # pragma: no cover
    from cached_property import cached_property  # type: ignore

WILDCARD = "#"
SINGLE_WILDCARD = "+"
SELECTORS = [
    "acp_names",
    "workload_names",
    "asset_names",
    "names",
]
IO_FIELDS = {
    "inputs": "sources",
    "outputs": "targets",
}


class QOS(IntEnum):
    """Quality-of-Service."""

    AT_MOST_ONCE = 0
    AT_LEAST_ONCE = 1
    EXACTLY_ONCE = 2

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any, ModelField, BaseConfig], Any]]:
        """Get pydantic validators."""

        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> int:
        """Validate data."""

        if isinstance(value, int):
            return cls(value)
        elif not isinstance(value, str):
            raise TypeError(f"Invalid value {value!r}") from None

        try:
            return cls.__members__[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid value {value!r}") from None


class Metric(Model):
    """Metric info."""

    class Config(Model.Config):
        """Pydantic config."""

        keep_untouched = (cached_property,)

    @validator(*SELECTORS, pre=True, always=True)
    def validate_selectors(cls, value: Any) -> Any:
        """Validate selectors."""

        if isinstance(value, str):
            return [value] if value != SINGLE_WILDCARD else []

        if not isinstance(value, Collection) or isinstance(value, Mapping):
            return value

        if any(not isinstance(x, str) for x in value):
            return value

        # wildcard
        if SINGLE_WILDCARD in value:
            return {*[]}

        return sorted(value)

    acp_names: Set[DNSName] = Field(
        {*[]},
        title="ACP Names",
        description="ACP names.",
    )
    workload_names: Set[DNSName] = Field(
        {*[]},
        title="Workload Names",
        description="Workload names.",
    )
    asset_names: Set[DottedName] = Field(
        {*[]},
        title="Asset Names",
        description="Asset names.",
    )
    names: Set[DottedName] = Field(
        {*[]},
        title="Names",
        description="Names.",
    )

    def match(self, x: Mapping[str, str]) -> bool:
        """Check if mapping matches metric info."""

        return all(x.get(k) in v for k, v in self.__dict__.items() if k in SELECTORS)

    @cached_property
    def combinations(self) -> Set[Tuple[str, ...]]:
        """Field combinations."""

        return {*product(*(sorted(getattr(self, field)) or [""] for field in SELECTORS))}

    @cached_property
    def topics(self) -> List[str]:
        """Topics."""

        values = product(
            *(sorted(getattr(self, field)) or [SINGLE_WILDCARD] for field in SELECTORS)
        )

        return ["/".join(x) for x in values]


class IO(Model):
    """IO."""

    class Config(Model.Config):
        """Pydantic config."""

        keep_untouched = (cached_property,)

    name: Identifier = Field(
        ...,
        title="Name",
        description="Name.",
    )
    data_type: DottedName = Field(
        ...,
        title="Data Type",
        description="Data type.",
    )
    metrics: List[Metric] = Field(
        [{}],
        title="Metrics",
        description="Metrics.",
    )

    @cached_property
    def topics(self) -> Set[str]:
        """Topics."""

        return {x for metric in self.metrics for x in metric.topics}

    @cached_property
    def combinations(self) -> Set[Tuple[str, ...]]:
        """Field combinations."""

        return {x for metric in self.metrics for x in metric.combinations}


class PubSubClientConfig(BaseSettings, Model):
    """Kelvin Pub-Sub Client Configuration."""

    class Config(BaseSettings.Config, Model.Config):
        """Pydantic configuration."""

        keep_untouched = (cached_property,)
        env_prefix = "KELVIN_PUBSUB_CLIENT__"

    broker_url: MQTTUrl = Field(
        "mqtt://kelvin-mqtt-broker",
        title="Kelvin Broker URI",
        description="Kelvin Broker URI. e.g. mqtt://localhost:1883",
    )
    client_id: Optional[str] = Field(
        None,
        title="Client ID",
        description="Client ID.",
    )

    qos: QOS = Field(
        QOS.AT_MOST_ONCE,
        title="Quality of Service",
        description="Quality of service for message delivery.",
    )
    sync: bool = Field(
        True,
        title="Default Connection",
        description="Default connection type: sync/async",
    )
    max_items: Optional[int] = Field(
        None,
        title="Max Items",
        description="Maximum number of items to hold in receive queue.",
    )

    @root_validator(pre=True)
    def validate_app_config(cls, values: Dict[str, Any]) -> Any:
        """Validate app configuration field and fill missing client configuration."""

        app_config = values.get("app_config")
        if app_config is None:
            return values

        if isinstance(app_config, str):
            app_config = Path(app_config.strip()).expanduser().resolve()
            if not app_config.is_file():
                raise ValueError(f"Invalid app configuration file {str(app_config)}")

        if isinstance(app_config, Mapping):
            pass
        elif isinstance(app_config, Path):
            app_config = values["app_config"] = yaml.safe_load(app_config.read_text())
        else:
            raise ValueError(f"Invalid app configuration type {type(app_config).__name__!r}")

        environment_config = app_config.get("environment", {})

        for name in ["acp_name", "workload_name"]:
            if name not in values and name in environment_config:
                values[name] = environment_config[name]

        kelvin_config = deep_get(app_config, "app.kelvin", {})

        for name in IO_FIELDS:
            if name not in values and name in kelvin_config:
                values[name] = kelvin_config[name]

        if "broker_url" not in values and "mqtt" in kelvin_config:
            mqtt_config = kelvin_config["mqtt"]
            ip = mqtt_config["ip"]
            port = mqtt_config.get("port", 1883)
            if "://" in ip:
                transport, _, host = ip.partition("://")
                if transport == "tcp":
                    scheme = "mqtt"
                elif transport == "ssl":
                    scheme = "mqtts"
                else:
                    raise ValueError(f"Unsupported transport {transport!r}")
            else:
                host = ip
                scheme = "mqtt"

            netloc = f"{host}:{port}"

            credentials = mqtt_config.get("credentials")
            if credentials:
                username = quote(credentials["username"])
                password = quote(credentials["password"])
                netloc = f"{username}:{password}@{netloc}"

            values["broker_url"] = urlunsplit((scheme, netloc, "", None, None))

        return values

    app_config: Dict[str, Any] = Field({}, title="Application Configuration")

    acp_name: str = Field(..., title="ACP Name", description="ACP name.")
    workload_name: str = Field(..., title="Workload Name", description="Workload name.")
    asset_name: Optional[str] = Field(None, title="Asset Name", description="Asset name.")

    @validator(*IO_FIELDS, pre=True, always=True)
    def validate_io(cls, value: Any, values: Dict[str, Any], field: ModelField) -> Any:
        """Validate IO."""

        if not value and field.name in values:
            value = values.pop(field.name)

        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            return value

        names: Set[str] = {
            item.get("name", "")
            for field_name in IO_FIELDS
            if field_name != field.name and isinstance(values.get(field_name), list)
            for item in values[field_name]
            if isinstance(item, Mapping)
        }
        errors: List[ErrorWrapper] = []

        value = [*value]
        for i, x in enumerate(value):
            if not isinstance(x, Mapping):
                continue

            name = x.get("name")
            if not isinstance(name, str):
                continue

            if name not in names:
                names |= {name}
            else:
                errors += [ErrorWrapper(ValueError(f"Name {name!r} must be unique"), loc=(i,))]

            metrics = x.get("metrics", ...)
            if metrics is ...:
                field_name = IO_FIELDS[field.name]
                if field_name in x:
                    x = value[i] = {**x}
                    metrics = x["metrics"] = x.pop(field_name)
                else:
                    metrics = None

            if field.name == "inputs" and not metrics:
                errors += [
                    ErrorWrapper(ValueError(f"Inputs must have at least one metric"), loc=(i,))
                ]

        if errors:
            raise ValidationError(errors, model=cast(Type[PubSubClientConfig], cls)) from None

        return value

    inputs: List[IO] = Field(
        [],
        title="Inputs",
        description="Message inputs.",
    )
    outputs: List[IO] = Field(
        [],
        title="Outputs",
        description="Message outputs.",
    )

    @cached_property
    def input_map(self) -> Dict[Tuple[str, ...], List[Tuple[str, str]]]:
        """Input map."""

        result: DefaultDict[Tuple[str, ...], Set[Tuple[str, str]]] = defaultdict(set)

        for io in self.inputs:
            for key_ in io.combinations:
                acp_name, workload_name, asset_name, name = key_
                key = (
                    acp_name or self.acp_name,
                    workload_name or self.workload_name,
                    asset_name or self.asset_name or "",
                    name or io.name,
                )
                result[key] |= {(io.name, io.data_type)}

        return {k: sorted(v) for k, v in result.items()}

    @cached_property
    def output_map(self) -> Dict[Tuple[str, ...], List[Tuple[str, str]]]:
        """Output map."""

        result: DefaultDict[Tuple[str, ...], Set[Tuple[str, str]]] = defaultdict(set)

        for io in self.outputs:
            for key_ in io.combinations:
                acp_name, workload_name, asset_name, name = key_
                key = (
                    acp_name or self.acp_name,
                    workload_name or self.workload_name,
                    asset_name or self.asset_name or "",
                    io.name,
                )
                result[key] |= {(name or io.name, io.data_type)}

        return {k: sorted(v) for k, v in result.items()}

    @cached_property
    def topics(self) -> List[str]:
        """Topics."""

        source = (self.acp_name, self.workload_name)

        def topic(x: Tuple[str, ...]) -> str:
            acp_name, workload_name, asset_name, name, *_ = x
            topic_type = "input" if (acp_name, workload_name) == source else "output"

            return f"{topic_type}/{'/'.join(v or SINGLE_WILDCARD for v in x)}"

        return [topic(x) for x in self.input_map]

    def __iter__(self) -> Iterator[str]:  # type: ignore
        """Key iterator."""

        return iter(self.__dict__)

import pathlib
from typing import List

from dagster import get_dagster_logger
from pydantic import (
    Field,
    PositiveInt,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.str_gen import get_config_str
from OpenStudioLandscapes.engine.config.models import FeatureBaseModel

from OpenStudioLandscapes.Syncthing import dist, constants


class Config(FeatureBaseModel):

    feature_name: str = dist.name

    group_name: str = constants.ASSET_HEADER["group_name"]

    key_prefixes: List[str] = constants.ASSET_HEADER["key_prefix"]

    syncthing_config_dir: pathlib.Path = Field(
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/syncthing"),
        description="The path to the `docker-compose.yml` file.",
    )

    syncthing_port_host: PositiveInt = Field(
        default=8787,
        description="The Syncthing host port.",
        frozen=False,
    )

    syncthing_port_container: PositiveInt = Field(
        default=8384,
        description="The Syncthing container port.",
        frozen=True,
    )

    syncthing_tcp_port_host: PositiveInt = Field(
        default=22022,
        description="The Syncthing TCP host port.",
        frozen=False,
    )

    syncthing_tcp_port_container: PositiveInt = Field(
        default=22000,
        description="The Syncthing TCP container port.",
        frozen=True,
    )

    syncthing_udp_port_host: PositiveInt = Field(
        default=22022,
        description="The Syncthing UDP host port.",
        frozen=False,
    )

    syncthing_udp_port_container: PositiveInt = Field(
        default=22000,
        description="The Syncthing UDP container port.",
        frozen=True,
    )

    syncthing_discovery_port_host: PositiveInt = Field(
        default=22027,
        description="The Syncthing discovery host port.",
        frozen=False,
    )

    syncthing_discovery_port_container: PositiveInt = Field(
        default=21027,
        description="The Syncthing discovery container port.",
        frozen=True,
    )

    syncthing_image: str = Field(
        default="docker.io/syncthing/syncthing",
        description="The Syncthing Docker image.",
    )

    # EXPANDABLE PATHS
    @property
    def syncthing_config_dir_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")
        LOGGER.debug(f"Expanding {self.syncthing_config_dir}...")
        ret = pathlib.Path(
            self.syncthing_config_dir.expanduser()
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


CONFIG_STR = get_config_str(
    Config=Config,
)


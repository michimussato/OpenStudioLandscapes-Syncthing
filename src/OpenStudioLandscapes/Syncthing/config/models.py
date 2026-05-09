import pathlib
from typing import List

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel
from pydantic import (
    Field,
    PositiveInt,
)

from OpenStudioLandscapes.Syncthing import (
    ASSET_HEADER,
    LOGGER,
    dist,
)


class Config(FeatureBaseModel):

    feature_name: str = dist.name

    group_name: str = ASSET_HEADER["group_name"]

    key_prefixes: List[str] = ASSET_HEADER["key_prefix"]

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
        default=22000,
        description="The Syncthing TCP host port.",
        frozen=False,
    )

    syncthing_udp_port_host: PositiveInt = Field(
        default=22000,
        description="The Syncthing UDP host port.",
        frozen=False,
    )

    syncthing_tcp_port_container: PositiveInt = Field(
        default=22000,
        description="The Syncthing TCP container port.",
        frozen=True,
    )

    syncthing_udp_port_container: PositiveInt = Field(
        default=22000,
        description="The Syncthing UDP container port.",
        frozen=True,
    )

    syncthing_discovery_port_host: PositiveInt = Field(
        default=21027,
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

    syncthing_umask: str = Field(
        default="022",
        description="The Syncthing UMASK Environment Variable.",
    )

    syncthing_puid: int = Field(
        default=1000,
        description="The Syncthing User ID.",
    )

    syncthing_pgid: int = Field(
        default=1000,
        description="The Syncthing Group ID.",
    )

    syncthing_pcap: str = Field(
        default="",
        description="The Syncthing PCAP Environment Variable. "
        "To grant Syncthing additional capabilities "
        "without running as root, use the PCAP environment "
        "variable with the same syntax as that "
        "for setcap(8). For example, "
        "cap_chown,cap_fowner+ep.",
    )

    syncthing_stguiaddress: str = Field(
        default="",
        description="The Syncthing GUI Address.",
    )

    # EXPANDABLE PATHS
    @property
    def syncthing_config_dir_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")
        LOGGER.debug(f"Expanding {self.syncthing_config_dir}...")
        ret = pathlib.Path(
            self.syncthing_config_dir.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


if __name__ == "__main__":
    CONFIG_STR = Config.get_docs()
else:
    import yaml

    CONFIG_STR = yaml.dump(
        Config.model_json_schema(mode="serialization"),
    )

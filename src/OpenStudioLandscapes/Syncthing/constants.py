__all__ = [
    "DOCKER_USE_CACHE",
    "SYNCTHING_CONFIG_INSIDE_CONTAINER",
    "ASSET_HEADER",
    "FEATURE_CONFIGS",
]

import pathlib
from typing import Any, Generator

from dagster import (
    AssetExecutionContext,
    AssetMaterialization,
    AssetOut,
    MetadataValue,
    Output,
    get_dagster_logger,
    multi_asset,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL
from OpenStudioLandscapes.engine.enums import (
    FeatureVolumeType,
    OpenStudioLandscapesConfig,
)

DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False
SYNCTHING_CONFIG_INSIDE_CONTAINER = False


GROUP = "Syncthing"
KEY = [GROUP]
FEATURE = f"OpenStudioLandscapes-{GROUP}".replace("_", "-")

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
}

# @formatter:off
FEATURE_CONFIGS = {
    OpenStudioLandscapesConfig.DEFAULT: {
        "DOCKER_USE_CACHE": DOCKER_USE_CACHE,
        # "HOSTNAME": "syncthing",
        "SYNCTHING_PORT_HOST": "8787",
        "SYNCTHING_PORT_CONTAINER": "8384",  # Default: 8384
        "SYNCTHING_TCP_PORT_HOST": "22022",
        "SYNCTHING_TCP_PORT_CONTAINER": "22000",  # Default: 22000
        "SYNCTHING_UDP_PORT_HOST": "22022",
        "SYNCTHING_UDP_PORT_CONTAINER": "22000",  # Default: 22000
        "SYNCTHING_DISCOVERY_PORT_HOST": "22027",
        "SYNCTHING_DISCOVERY_PORT_CONTAINER": "21027",  # Default: 21027
        "SYNCTHING_CONFIG_DIR": {
            #################################################################
            # Syncthing config dir will be created in (hardcoded):
            # "KITSU_DATABASE_INSTALL_DESTINATION" / "postgresql" / "14" / "main"
            # Kitsu Previews folder will be created in (hardcoded):
            # "KITSU_DATABASE_INSTALL_DESTINATION" / "previews"
            #################################################################
            #################################################################
            # Inside Landscape:
            FeatureVolumeType.CONTAINED: pathlib.Path(
                "{DOT_LANDSCAPES}",
                "{LANDSCAPE}",
                f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
                "data",
                "syncthing",
            ).as_posix(),
            #################################################################
            # Shared:
            FeatureVolumeType.SHARED: pathlib.Path(
                "{DOT_LANDSCAPES}",
                "{DOT_SHARED_VOLUMES}",
                f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
                "data",
                "syncthing",
            ).as_posix(),
        }[FeatureVolumeType.CONTAINED],
    }
}
# @formatter:on


# Todo:
#  - [ ] move to common_assets
@multi_asset(
    name=f"constants_{GROUP}",
    outs={
        "NAME": AssetOut(
            **ASSET_HEADER,
            dagster_type=str,
            description="",
        ),
        "FEATURE_CONFIGS": AssetOut(
            **ASSET_HEADER,
            dagster_type=dict,
            description="",
        ),
        "DOCKER_COMPOSE": AssetOut(
            **ASSET_HEADER,
            dagster_type=pathlib.Path,
            description="",
        ),
    },
)
def constants_multi_asset(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[OpenStudioLandscapesConfig, dict[str, bool | str]]]
    | AssetMaterialization
    | Output[Any]
    | Output[pathlib.Path]
    | Any,
    None,
    None,
]:
    """ """

    yield Output(
        output_name="FEATURE_CONFIGS",
        value=FEATURE_CONFIGS,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("FEATURE_CONFIGS"),
        metadata={
            "__".join(
                context.asset_key_for_output("FEATURE_CONFIGS").path
            ): MetadataValue.json(FEATURE_CONFIGS),
        },
    )

    yield Output(
        output_name="NAME",
        value=__name__,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("NAME"),
        metadata={
            "__".join(context.asset_key_for_output("NAME").path): MetadataValue.path(
                __name__
            ),
        },
    )

    docker_compose = pathlib.Path(
        "{DOT_LANDSCAPES}",
        "{LANDSCAPE}",
        f"{ASSET_HEADER['group_name']}__{'_'.join(ASSET_HEADER['key_prefix'])}",
        "__".join(context.asset_key_for_output("DOCKER_COMPOSE").path),
        "docker_compose",
        "docker-compose.yml",
    )

    yield Output(
        output_name="DOCKER_COMPOSE",
        value=docker_compose,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("DOCKER_COMPOSE"),
        metadata={
            "__".join(
                context.asset_key_for_output("DOCKER_COMPOSE").path
            ): MetadataValue.path(docker_compose),
        },
    )

__all__ = [
    "DOCKER_USE_CACHE",
    "SYNCTHING_CONFIG_INSIDE_CONTAINER",
    "ASSET_HEADER",
    "FEATURE_CONFIGS",
]

import pathlib
from typing import Generator, Any

from dagster import (
    multi_asset,
    AssetOut,
    AssetMaterialization,
    AssetExecutionContext,
    Output,
    MetadataValue,
    get_dagster_logger,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL
from OpenStudioLandscapes.engine.enums import OpenStudioLandscapesConfig

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
        "SYNCTHING_PORT_HOST": "8787",
        "SYNCTHING_PORT_CONTAINER": "8384",
        "SYNCTHING_CONFIG_DIR": {
            #################################################################
            # Syncthing config dir will be created in (hardcoded):
            # "KITSU_DATABASE_INSTALL_DESTINATION" / "postgresql" / "14" / "main"
            # Kitsu Previews folder will be created in (hardcoded):
            # "KITSU_DATABASE_INSTALL_DESTINATION" / "previews"
            #################################################################
            #################################################################
            # Inside Landscape:
            "default": pathlib.Path(
                "{DOT_LANDSCAPES}",
                "{LANDSCAPE}",
                f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
                "data",
                "syncthing",
            ).as_posix(),
        }["default"],
        # "GRAFANA_PORT_HOST": "3030",
        # "GRAFANA_PORT_CONTAINER": "3030",
        # "GRAFANA_GRAFANA_INI": pathlib.Path(
        #     get_git_root(pathlib.Path(__file__)),
        #     "configs",
        #     *KEY,
        #     "etc",
        #     "grafana",
        #     "grafana.ini",
        # ).as_posix(),
        # "GRAFANA_DEFAULTS_INI": pathlib.Path(
        #     get_git_root(pathlib.Path(__file__)),
        #     "configs",
        #     *KEY,
        #     "usr",
        #     "share",
        #     "grafana",
        #     "conf",
        #     "defaults.ini",
        # ).as_posix(),
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
    Output[dict[OpenStudioLandscapesConfig, dict[str, bool | str]]] | AssetMaterialization | Output[Any] | Output[
        pathlib.Path] | Any, None, None]:
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
            "__".join(
                context.asset_key_for_output("NAME").path
            ): MetadataValue.path(__name__),
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

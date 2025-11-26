import copy
import json
import pathlib
from typing import Any, Generator

import yaml
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    MetadataValue,
    Output,
    asset,
)
from OpenStudioLandscapes.engine.common_assets.compose import get_compose
from OpenStudioLandscapes.engine.common_assets.constants import get_constants
from OpenStudioLandscapes.engine.common_assets.docker_compose_graph import (
    get_docker_compose_graph,
)
from OpenStudioLandscapes.engine.common_assets.docker_config import get_docker_config
from OpenStudioLandscapes.engine.common_assets.docker_config_json import (
    get_docker_config_json,
)
from OpenStudioLandscapes.engine.common_assets.env import get_env
from OpenStudioLandscapes.engine.common_assets.feature_out import get_feature_out
from OpenStudioLandscapes.engine.common_assets.group_in import get_group_in
from OpenStudioLandscapes.engine.common_assets.group_out import get_group_out
from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *

from OpenStudioLandscapes.Syncthing.constants import *

constants = get_constants(
    ASSET_HEADER=ASSET_HEADER,
)


docker_config = get_docker_config(
    ASSET_HEADER=ASSET_HEADER,
)


group_in = get_group_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_PARENT=ASSET_HEADER_BASE,
    input_name=str(GroupIn.BASE_IN),
)


env = get_env(
    ASSET_HEADER=ASSET_HEADER,
)


group_out = get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph = get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose = get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out = get_feature_out(
    ASSET_HEADER=ASSET_HEADER,
    feature_out_ins={
        "env": dict,
        "compose": dict,
        "group_in": dict,
    },
)


docker_config_json = get_docker_config_json(
    ASSET_HEADER=ASSET_HEADER,
)


@asset(
    **ASSET_HEADER,
)
def compose_networks(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[str, dict[str, dict[str, str]]]] | AssetMaterialization, None, None
]:

    # https://github.com/syncthing/syncthing/blob/main/README-Docker.md#discovery
    # for host mode, set
    # compose_network_mode = ComposeNetworkMode.HOST
    compose_network_mode = DockerComposePolicies.NETWORK_MODE.DEFAULT

    if compose_network_mode is DockerComposePolicies.NETWORK_MODE.DEFAULT:
        docker_dict = {
            "networks": {
                "syncthing": {
                    "name": "network_syncthing",
                },
            },
        }

    else:
        docker_dict = {
            "network_mode": compose_network_mode.value,
        }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_dict": MetadataValue.md(
                f"```json\n{json.dumps(docker_dict, indent=2)}\n```"
            ),
            "docker_yaml": MetadataValue.md(f"```shell\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_networks"]),
        ),
    },
)
def compose_syncthing(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    network_dict = {}
    ports_dict = {}

    if "networks" in compose_networks:
        network_dict = {"networks": list(compose_networks.get("networks", {}).keys())}
        ports_dict = {
            "ports": [
                f"{env['SYNCTHING_PORT_HOST']}:{env['SYNCTHING_PORT_CONTAINER']}",  # Web UI
                f"{env['SYNCTHING_TCP_PORT_HOST']}:{env['SYNCTHING_TCP_PORT_CONTAINER']}/tcp",  # TCP file transfers
                f"{env['SYNCTHING_UDP_PORT_HOST']}:{env['SYNCTHING_UDP_PORT_CONTAINER']}/udp",  # QUIC file transfers
                f"{env['SYNCTHING_DISCOVERY_PORT_HOST']}:{env['SYNCTHING_DISCOVERY_PORT_CONTAINER']}/udp",  # Receive local discovery broadcasts
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {"network_mode": compose_networks["network_mode"]}

    volumes_dict = {"volumes": []}

    if not SYNCTHING_CONFIG_INSIDE_CONTAINER:

        syncthing_config_dir_host = pathlib.Path(env["SYNCTHING_CONFIG_DIR"])
        syncthing_config_dir_host.mkdir(parents=True, exist_ok=True)

        volumes_dict["volumes"].insert(
            0,
            f"{syncthing_config_dir_host.as_posix()}:/var/syncthing",
        )

    # For portability, convert absolute volume paths to relative paths

    _volume_relative = []

    for v in volumes_dict["volumes"]:

        host, container = v.split(":", maxsplit=1)

        volume_dir_host_rel_path = get_relative_path_via_common_root(
            context=context,
            path_src=pathlib.Path(env["DOCKER_COMPOSE"]),
            path_dst=pathlib.Path(host),
            path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
        )

        _volume_relative.append(
            f"{volume_dir_host_rel_path.as_posix()}:{container}",
        )

    volumes_dict = {
        "volumes": [
            *_volume_relative,
        ]
    }

    service_name = "syncthing"
    container_name, host_name = get_docker_compose_names(
        context=context,
        service_name=service_name,
        landscape_id=env.get("LANDSCAPE", "default"),
        domain_lan=env.get("OPENSTUDIOLANDSCAPES__DOMAIN_LAN"),
    )
    # container_name = "--".join([service_name, env.get("LANDSCAPE", "default")])
    # host_name = ".".join(
    #     [service_name, env["OPENSTUDIOLANDSCAPES__DOMAIN_LAN"]]
    # )

    docker_dict = {
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
                "domainname": env["OPENSTUDIOLANDSCAPES__DOMAIN_LAN"],
                # "restart": DockerComposePolicies.RESTART_POLICY.ALWAYS.value,
                "image": "docker.io/syncthing/syncthing",
                "restart": DockerComposePolicies.RESTART_POLICY.UNLESS_STOPPED.value,
                "environment": {
                    "PUID": "1000",
                    "PGID": "1000",
                },
                # "healthcheck": {
                #     "test": ["CMD", "curl", "-f", f"http://localhost:{env_base.get('DAGSTER_DEV_PORT_CONTAINER')}"],
                #     "test": "curl -fkLsS -m 2 127.0.0.1:8384/rest/noauth/health | grep -o --color=never OK || exit 1",
                #     "interval": "1m",
                #     "timeout": "10s",
                #     "retries": "3",
                # },
                # "command": [
                #     "--workspace",
                #     env_base.get('DAGSTER_WORKSPACE'),
                #     "--host",
                #     env_base.get('DAGSTER_HOST'),
                #     "--port",
                #     env_base.get('DAGSTER_DEV_PORT_CONTAINER'),
                # ],
                **copy.deepcopy(volumes_dict),
                **copy.deepcopy(network_dict),
                **copy.deepcopy(ports_dict),
            },
        },
    }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
            # Todo: "cmd_docker_run": MetadataValue.path(cmd_list_to_str(cmd_docker_run)),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "compose_syncthing": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_syncthing"]),
        ),
    },
)
def compose_maps(
    context: AssetExecutionContext,
    **kwargs,  # pylint: disable=redefined-outer-name
) -> Generator[Output[list[dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    context.log.info(ret)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={},
)
def cmd_extend(
    context: AssetExecutionContext,
) -> Generator[Output[list[Any]] | AssetMaterialization | Any, Any, None]:

    ret = []

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={},
)
def cmd_append(
    context: AssetExecutionContext,
) -> Generator[Output[dict[str, list[Any]]] | AssetMaterialization | Any, Any, None]:

    ret = {"cmd": [], "exclude_from_quote": []}

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )

[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Syncthing](#feature-openstudiolandscapes-syncthing)
   1. [Brief](#brief)
   2. [Clone](#clone)
      1. [Clone and Install](#clone-and-install)
   3. [Configure](#configure)
      1. [Default Configuration](#default-configuration)
   4. [Local Development/Unit Testing/Debugging](#local-developmentunit-testingdebugging)
2. [External Resources](#external-resources)
   1. [Official Documentation](#official-documentation)
      1. [Elevated Permissions](#elevated-permissions)
      2. [Ports](#ports)
3. [Community](#community)

***

This `README.md` was dynamically created with [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).

***

# Feature: OpenStudioLandscapes-Syncthing

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

> [!NOTE]
> 
> You feel like writing your own Feature? Go and check out the 
> [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Clone

Clone this repository into `OpenStudioLandscapes/.features` (assuming the current working directory to be the Git repository root `./OpenStudioLandscapes`):

```shell
# cd OpenStudioLandscapes
source .venv/bin/activate
openstudiolandscapes clone-feature --repo=https://github.com/michimussato/OpenStudioLandscapes-Syncthing.git
deactivate
# Check the resulting console output for installation instructions
```

### Clone and Install

```shell
# cd OpenStudioLandscapes
source .venv/bin/activate
openstudiolandscapes clone-feature --repo=https://github.com/michimussato/OpenStudioLandscapes-Syncthing.git \
    && pip install --editable ./.features/OpenStudioLandscapes-Syncthing
deactivate
```

For more info on `pip` see [VCS Support of `pip`](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Configure

OpenStudioLandscapes will search for a local config store. The default location is `~/.config/OpenStudioLandscapes/config-store/` but you can specify a different location if you need to.

> [!TIP]
> 
> To specify a config store location different from
> the default location, check out the OpenStudioLandscapes 
> [CLI Section](https://github.com/michimussato/OpenStudioLandscapes#cli)
> to find out how to do that.

A local config store location will be created if it doesn't exist, together with the `config.yml` files for each individual Feature.

> [!TIP]
> 
> The config store root will be initialized as a local Git
> controlled repository. This makes it easy to track changes
> you made to the `config.yml`.

The following settings are available in `OpenStudioLandscapes-Syncthing` and are based on [`OpenStudioLandscapes-Syncthing/tree/main/src/OpenStudioLandscapes/Syncthing/config/models.py`](https://github.com/michimussato/OpenStudioLandscapes-Syncthing/tree/main/src/OpenStudioLandscapes/Syncthing/config/models.py).

### Default Configuration

<details open>
<summary><code>config.yml</code></summary>


```yaml
properties:
  compose_scope:
    default: default
    examples:
    - default
    - license_server
    - worker
    title: Compose Scope
    type: string
  docker_compose:
    default: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/docker_compose/docker-compose.yml'
    description: The path to the `docker-compose.yml` file.
    format: path
    title: Docker Compose
    type: string
  enabled:
    default: true
    description: Whether the Feature is enabled or not.
    title: Enabled
    type: boolean
  env:
    additionalProperties: true
    title: Env
    type: object
  feature_name:
    default: OpenStudioLandscapes-Syncthing
    title: Feature Name
    type: string
  group_name:
    default: OpenStudioLandscapes_Syncthing
    title: Group Name
    type: string
  key_prefixes:
    default:
    - OpenStudioLandscapes_Syncthing
    items:
      type: string
    title: Key Prefixes
    type: array
  local_bind_volumes:
    description: Here you can define Feature specific, arbitrary, absolute bind volume
      mappings.
    items:
      type: string
    title: Local Bind Volumes
    type: array
  local_environment_variables:
    additionalProperties:
      type: string
    description: Here you can define Feature specific, arbitrary environment variables.
    title: Local Environment Variables
    type: object
  syncthing_config_dir:
    default: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/syncthing'
    description: The path to the `docker-compose.yml` file.
    format: path
    title: Syncthing Config Dir
    type: string
  syncthing_discovery_port_container:
    default: 21027
    description: The Syncthing discovery container port.
    exclusiveMinimum: 0
    title: Syncthing Discovery Port Container
    type: integer
  syncthing_discovery_port_host:
    default: 21027
    description: The Syncthing discovery host port.
    exclusiveMinimum: 0
    title: Syncthing Discovery Port Host
    type: integer
  syncthing_image:
    default: docker.io/syncthing/syncthing
    description: The Syncthing Docker image.
    title: Syncthing Image
    type: string
  syncthing_pcap:
    default: ''
    description: The Syncthing PCAP Environment Variable. To grant Syncthing additional
      capabilities without running as root, use the PCAP environment variable with
      the same syntax as that for setcap(8). For example, cap_chown,cap_fowner+ep.
    title: Syncthing Pcap
    type: string
  syncthing_pgid:
    default: 1000
    description: The Syncthing Group ID.
    title: Syncthing Pgid
    type: integer
  syncthing_port_container:
    default: 8384
    description: The Syncthing container port.
    exclusiveMinimum: 0
    title: Syncthing Port Container
    type: integer
  syncthing_port_host:
    default: 8787
    description: The Syncthing host port.
    exclusiveMinimum: 0
    title: Syncthing Port Host
    type: integer
  syncthing_puid:
    default: 1000
    description: The Syncthing User ID.
    title: Syncthing Puid
    type: integer
  syncthing_stguiaddress:
    default: ''
    description: The Syncthing GUI Address.
    title: Syncthing Stguiaddress
    type: string
  syncthing_tcp_port_container:
    default: 22000
    description: The Syncthing TCP container port.
    exclusiveMinimum: 0
    title: Syncthing Tcp Port Container
    type: integer
  syncthing_tcp_port_host:
    default: 22000
    description: The Syncthing TCP host port.
    exclusiveMinimum: 0
    title: Syncthing Tcp Port Host
    type: integer
  syncthing_udp_port_container:
    default: 22000
    description: The Syncthing UDP container port.
    exclusiveMinimum: 0
    title: Syncthing Udp Port Container
    type: integer
  syncthing_udp_port_host:
    default: 22000
    description: The Syncthing UDP host port.
    exclusiveMinimum: 0
    title: Syncthing Udp Port Host
    type: integer
  syncthing_umask:
    default: '022'
    description: The Syncthing UMASK Environment Variable.
    title: Syncthing Umask
    type: string
title: Config
type: object

```

</details>


## Local Development/Unit Testing/Debugging

This is for isolated development, unit testing and debugging. Instead of the [`OpenStudioLandscapes-Syncthing/tree/main/src/OpenStudioLandscapes/Syncthing/definitions.py`](https://github.com/michimussato/OpenStudioLandscapes-Syncthing/tree/main/src/OpenStudioLandscapes/Syncthing/definitions.py), the accompanying [`OpenStudioLandscapes-Syncthing/tree/main/workspace.yaml`](https://github.com/michimussato/OpenStudioLandscapes-Syncthing/tree/main/workspace.yaml) loads the [`OpenStudioLandscapes-Syncthing/tree/main/src/OpenStudioLandscapes/Syncthing/_definitions_with_upstream_specs.py`](https://github.com/michimussato/OpenStudioLandscapes-Syncthing/tree/main/src/OpenStudioLandscapes/Syncthing/_definitions_with_upstream_specs.py) which also contains [`AssetSpec`](https://release-1-9-13.archive.dagster-docs.io/api/dagster/assets#dagster.AssetSpec) definitions for upstream dependencies as [external assets](https://release-1-9-13.archive.dagster-docs.io/guides/build/assets/external-assets).

```shell
# cd ./.features/OpenStudioLandscapes-Syncthing
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools setuptools_scm wheel
pip install --editable .[dev]
dagster dev --workspace workspace.yaml
```

***

# External Resources

[![Logo Syncthing ](https://syncthing.net/img/logo-horizontal.svg)](https://syncthing.net/)

Syncthing is a continuous file synchronization program. It synchronizes files between two or more computers in real time, safely protected from prying eyes. Your data is your data alone and you deserve to choose where it is stored, whether it is shared with some third party, and how it’s transmitted over the internet.

## Official Documentation

- [Website](https://syncthing.net/)
- [Docs](https://docs.syncthing.net/)
- [GitHub](https://github.com/syncthing/syncthing)
- [Syncthing Docker Readme](https://github.com/syncthing/syncthing/blob/main/README-Docker.md)

### Elevated Permissions

- [Elevated permissions](https://docs.syncthing.net/advanced/folder-sync-ownership.html#elevated-permissions)

### Ports

- [Firewall Setup](https://docs.syncthing.net/users/firewall.html#firewall-setup)

***

# Community

| Feature                                   | GitHub                                                                                                                                                 | Discord                                                                      |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| OpenStudioLandscapes                      | [https://github.com/michimussato/OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                           | [# openstudiolandscapes-general](https://discord.gg/F6bDRWsHac)              |
| OpenStudioLandscapes-Ayon                 | [https://github.com/michimussato/OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                                 | [# openstudiolandscapes-ayon](https://discord.gg/gd6etWAF3v)                 |
| OpenStudioLandscapes-Dagster              | [https://github.com/michimussato/OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                           | [# openstudiolandscapes-dagster](https://discord.gg/jwB3DwmKvs)              |
| OpenStudioLandscapes-Deadline-10-2        | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2)               | [# openstudiolandscapes-deadline-10-2](https://discord.gg/p2UjxHk4Y3)        |
| OpenStudioLandscapes-Deadline-10-2-Worker | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker) | [# openstudiolandscapes-deadline-10-2-worker](https://discord.gg/ttkbfkzUmf) |
| OpenStudioLandscapes-Flamenco             | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco](https://github.com/michimussato/OpenStudioLandscapes-Flamenco)                         | [# openstudiolandscapes-flamenco](https://discord.gg/EPrX5fzBCf)             |
| OpenStudioLandscapes-Flamenco-Worker      | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker](https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker)           | [# openstudiolandscapes-flamenco-worker](https://discord.gg/Sa2zFqSc4p)      |
| OpenStudioLandscapes-Grafana              | [https://github.com/michimussato/OpenStudioLandscapes-Grafana](https://github.com/michimussato/OpenStudioLandscapes-Grafana)                           | [# openstudiolandscapes-grafana](https://discord.gg/gEDQ8vJWDb)              |
| OpenStudioLandscapes-Kitsu                | [https://github.com/michimussato/OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                               | [# openstudiolandscapes-kitsu](https://discord.gg/6cc6mkReJ7)                |
| OpenStudioLandscapes-LikeC4               | [https://github.com/michimussato/OpenStudioLandscapes-LikeC4](https://github.com/michimussato/OpenStudioLandscapes-LikeC4)                             | [# openstudiolandscapes-likec4](https://discord.gg/qAYYsKYF6V)               |
| OpenStudioLandscapes-OpenCue              | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue](https://github.com/michimussato/OpenStudioLandscapes-OpenCue)                           | [# openstudiolandscapes-opencue](https://discord.gg/3DdCZKkVyZ)              |
| OpenStudioLandscapes-OpenCue-Worker       | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker](https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker)             | [# openstudiolandscapes-opencue-worker](https://discord.gg/n9fxxhHa3V)       |
| OpenStudioLandscapes-RustDeskServer       | [https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer](https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer)             | [# openstudiolandscapes-rustdeskserver](https://discord.gg/nJ8Ffd2xY3)       |
| OpenStudioLandscapes-Syncthing            | [https://github.com/michimussato/OpenStudioLandscapes-Syncthing](https://github.com/michimussato/OpenStudioLandscapes-Syncthing)                       | [# openstudiolandscapes-syncthing](https://discord.gg/upb9MCqb3X)            |
| OpenStudioLandscapes-Template             | [https://github.com/michimussato/OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template)                         | [# openstudiolandscapes-template](https://discord.gg/J59GYp3Wpy)             |
| OpenStudioLandscapes-VERT                 | [https://github.com/michimussato/OpenStudioLandscapes-VERT](https://github.com/michimussato/OpenStudioLandscapes-VERT)                                 | [# openstudiolandscapes-vert](https://discord.gg/EPrX5fzBCf)                 |
| OpenStudioLandscapes-filebrowser          | [https://github.com/michimussato/OpenStudioLandscapes-filebrowser](https://github.com/michimussato/OpenStudioLandscapes-filebrowser)                   | [# openstudiolandscapes-filebrowser](https://discord.gg/stzNsZBmwk)          |
| OpenStudioLandscapes-n8n                  | [https://github.com/michimussato/OpenStudioLandscapes-n8n](https://github.com/michimussato/OpenStudioLandscapes-n8n)                                   | [# openstudiolandscapes-n8n](https://discord.gg/yFYrG999wE)                  |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

Last changed: **2026-05-07 19:19:26 UTC**
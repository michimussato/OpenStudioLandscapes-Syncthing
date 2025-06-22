from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Syncthing.assets
import OpenStudioLandscapes.Syncthing.constants

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Syncthing.assets],
)

constants = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Syncthing.constants],
)


defs = Definitions(
    assets=[
        *assets,
        *constants,
    ],
)

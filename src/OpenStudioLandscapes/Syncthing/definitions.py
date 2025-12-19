from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Syncthing.assets

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Syncthing.assets],
)


defs = Definitions(
    assets=[
        *assets,
    ],
)

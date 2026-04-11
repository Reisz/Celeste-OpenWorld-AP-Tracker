# Celeste-OpenWorld-AP-Tracker

[PopTracker](https://poptracker.github.io/) pack for
[Celeste Archipelago Open World](https://archipelago.gg/games/Celeste%20(Open%20World)/info/en)
([AP World](https://github.com/ArchipelagoMW/Archipelago/tree/main/worlds/celeste_open_world),
[Mod](https://github.com/PoryGoneDev/Celeste-Archipelago-Open-World)).

## Pack Features

- Supports A-, B- and C-Sides of all chapters, except Farewell
- Auto-tracking and logic for the following location types:
  - Strawberries
  - Keys
  - Level Clears / Crystal Hearts
  - Golden Strawberries (including the Winged Golden Strawberry)
- Auto-tracking for the following item types:
  - Interactables (e.g. Dash Crystals, Traffic Blocks)
  - Keys (Keysanity)

## Planned Features

- Overview map ([#52](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/52))
- Support Farewell ([#28](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/28))
- Item auto-tracking for checkpoints ([#40](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/40))
- Item auto-tracking for summit gems ([#45](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/45))
- Checkpointsanity ([#42](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/42))
- Binosanity ([#44](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/44))
- Gemsanity ([#46](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/46))
- Carsanity ([#47](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/47))
- Roomsanity ([#48](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/48))
- Automated tab switching ([#50](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/50))
- Support for skips ([#51](https://github.com/Reisz/Celeste-OpenWorld-AP-Tracker/issues/51))

## Working on the pack

All workflow processes are encoded as [`justfile`](justfile) recipes.

Use `just --list` to see available recipes.

> [!NOTE]
> Windows users should check out the repository with `core.autocrlf = false`,
> as most formatting tools only accept Unix-style line endings.

### Dependencies

This repository uses [`mise`](https://mise.jdx.dev/) to manage required tools. You can either use
one of the `mise` [activation methods](https://mise.jdx.dev/getting-started.html#activate-mise),
or run recipes using `mise exec -- just`.

#### System Dependencies

The following applications should be available as system packages on any Linux distribution
or come with Git Bash on Windows.

- `unzip` - For unzipping downloaded resources
- `diffutils` - `diff` for reproducibility test
- `findutils` - `xargs` for image download
- `zip` - For creating the final pack
- `curl` - For resource downloads

### LSP Support

#### Lua

This repository includes a `.luarc.json` file for [LuaLS](https://luals.github.io/).
PopTracker Lua stubs need to be downloaded using the `just download` recipe.

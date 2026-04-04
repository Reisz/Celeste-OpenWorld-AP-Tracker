# Celeste-OpenWorld-AP-Tracker

[PopTracker](https://poptracker.github.io/) pack for
[Celeste OpenWorld AP](https://archipelago.gg/games/Celeste%20(Open%20World)/info/en).

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
- `findutils` - `xargs` for image download
- `zip` - For creating the final pack
- `curl` - For resource downloads

### LSP Support

#### Lua

This repository includes a `.luarc.json` file for [LuaLS](https://luals.github.io/).
PopTracker Lua stubs need to be downloaded using the `just download` recipe.

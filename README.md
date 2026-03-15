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

Each of following applications is required for at least one recipe.

If you do not need to run all recipes, check the [`justfile`](justfile) source
to see which applications are needed for specific recipes.

#### Core Dependencies

The following applications need to be manually installed.

> [!NOTE]
> Windows users need to make sure that all listed dependencies and `sh.exe` from Git Bash
> are accessible via the system `PATH`.

- [`just`](https://just.systems/) - Project workflow
  - [Installation instructions](https://github.com/casey/just?tab=readme-ov-file#installation)
- [`uv`](https://docs.astral.sh/uv/) - Python project management
  - [Installation instructions](https://docs.astral.sh/uv/getting-started/installation/)
- [`curl`](https://curl.se/) - Resource downloads
  - [Installation instructions](https://curl.se/download.html)
- [`jq`](https://jqlang.org/) - JSON processing
  - [Installation instructions](https://jqlang.org/download/)
- [`fd`](https://github.com/sharkdp/fd) - `find` with `.gitignore` support
  - [Installation instructions](https://github.com/sharkdp/fd?tab=readme-ov-file#installation)
- [`stylua`](https://github.com/JohnnyMorganz/StyLua) - Lua format check
  - [Installation instructions](https://github.com/JohnnyMorganz/StyLua?tab=readme-ov-file#installation)
- [`taplo`](https://taplo.tamasfe.dev/) - TOML format check
  - [Binaries](https://taplo.tamasfe.dev/cli/installation/binary.html),
[Repositories](https://repology.org/project/taplo/versions),
[Cargo](https://taplo.tamasfe.dev/cli/installation/cargo.html),
[NPM](https://taplo.tamasfe.dev/cli/installation/npm.html)

#### System Dependencies

The following applications should be available as system packages on any Linux distribution
or come with Git Bash on Windows.

- `unzip` - For unzipping downloaded resources
- `findutils` - `xargs` for image download
- `zip` - For creating the final pack

### LSP Support

#### Lua

This repository includes a `.luarc.json` file for [LuaLS](https://luals.github.io/).
PopTracker Lua stubs need to be downloaded using the `just download` recipe.

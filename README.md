# Celeste-OpenWorld-AP-Tracker

[PopTracker](https://poptracker.github.io/) pack for
[Celeste OpenWorld AP](https://archipelago.gg/games/Celeste%20(Open%20World)/info/en).

## Working on the pack

All workflow processes are encoded in the [`justfile`](justfile).
Use `just --list` to see available recipes.

### Required software

- [`just`](https://just.systems/)
- [`uv`](https://docs.astral.sh/uv/)
- [`jq`](https://jqlang.org/)
- [`curl`](https://curl.se/)
- [`fd`](https://github.com/sharkdp/fd)
- `zip` / `unzip`
- `cmp`
- `xargs`

#### Windows Installation Troubleshooting

- [just](https://just.systems/) - If installed and the `just` command is failing
with `Recipe 'check' could not be run because just could not find the shell: program not found`
, you need to add Git For Windows' `sh.exe` to your System PATH.

- [uv](https://docs.astral.sh/uv/) - If installed and the `uv` command is failing with
`/usr/bin/bash: line 1: uv: command not found`, you need to add `uv` to your System PATH.
- [jq](https://jqlang.org/) - PowerShell installer: `winget install jqlang.jq`
- [fd](https://github.com/sharkdp/fd) - PowerShell installer: `winget install sharkdp.fd`

#### Windows Just Receipe Troubleshooting

Recipe: check

If an initial run error produces something like
`cmp: EOF on ‘./tracker/layouts/items_layout.json’ after byte 9012, in line 299`,
make sure you files end with an empty newline character
(e.g. If you have a JSON file `{}`, make sure it actually looks like `{}\n`).

`just --fmt --unstable --check` may produce a justfile which exactly matches
to the human eye but has windows/linux differences. You can run
`just --fmt--unstable` manually to produce an exactly matching file
before running the check.

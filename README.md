# 🐼 PandaCode

**English** | [Türkçe](README.tr.md)

**A simple, Turkish-first terminal coding agent, built on [oh-my-pi (omp)](https://github.com/can1357/oh-my-pi).**

omp is a powerful coding agent harness with well over a hundred commands. PandaCode keeps its engine as is and changes the experience around it: a command-line tool that feels as easy as a desktop app. You see the everyday commands, the keys you need sit right under the prompt, and the interface speaks Turkish.

> **Status:** early. PandaCode is built and tested on Windows by its author. Expect rough edges, and parts of the interface that are still in English.

## What PandaCode adds

| | |
|---|---|
| **Simple mode** | The `/` picker lists 16 everyday commands instead of the full set. Nothing is removed: every omp command still runs when typed, and `/gelismis` (or `/advanced`) toggles the full list. |
| **Command palette** | <kbd>Ctrl</kbd>+<kbd>K</kbd> on an empty prompt opens a searchable list of commands with their descriptions. With text in the prompt, <kbd>Ctrl</kbd>+<kbd>K</kbd> still deletes to the end of the line. |
| **Shortcut bar** | One dim row under the prompt shows the keys that matter right now: commands, model, thinking level, history and exit while idle; stop and details while the agent works. |
| **Turkish interface** | Command descriptions, tips, the shortcut bar, selectors and setup headings are in Turkish by default. Switch with `/settings` → PandaCode → *Arayüz Dili* (Turkish / English). |
| **Three-step setup** | First run asks only for sign-in, model and theme. |
| **`pandacode` command** | A launcher that runs this checkout from any folder, next to an installed `omp` without touching it. |
| **Panda** | A panda logo and the PandaCode name on the welcome and setup screens. |

All of these live in `/settings` under the **PandaCode** group.

## Install from source

You need [Bun](https://bun.sh) and Git.

```bash
git clone https://github.com/pandakingpunc/pandacode.git
cd pandacode
bun install
```

PandaCode needs omp's native addon (`pi_natives`), which is not checked in. Get it one of two ways:

- **Build it:** `bun run build:native`. This needs the Rust toolchain pinned in `rust-toolchain.toml` and your platform's C/C++ build tools.
- **Copy it from an installed omp of the same version (18.12.6):** copy `~/.omp/natives/18.12.6/pi_natives.<platform>.node` into `packages/natives/native/`.

Then install the launcher and start:

```bash
bun run install:pandacode
pandacode
```

`install:pandacode` writes `pandacode` (and `pandacode.cmd` on Windows) into Bun's global bin folder. It never overwrites a file it did not write; `bun run install:pandacode --uninstall` removes them.

## Good to know

- Under the hood PandaCode is still omp 18.12.6. Settings, sessions and logins live in `~/.omp`, so an existing omp setup carries over, and `pandacode --version` prints `omp/…`.
- The Turkish interface is partial for now. The settings panel, the bodies of the setup steps and most status messages are still in English.
- For omp's own features (tools, providers, subagents, LSP, the debugger and more), see the [oh-my-pi README](https://github.com/can1357/oh-my-pi#readme).

## Credits and license

PandaCode is a fork of [oh-my-pi](https://github.com/can1357/oh-my-pi) by Can Bölük and Stencil Labs, which itself builds on Mario Zechner's pi. All the heavy lifting is theirs.

PandaCode changes are by [Mustafa Karatum](https://github.com/pandakingpunc).

Released under the [MIT License](LICENSE), like omp. The original copyright notices are kept in [LICENSE](LICENSE).

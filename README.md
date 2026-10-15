# Snake 🐍

Snake, in two flavours:

- **Python (pygame-ce)** — the main game, compiled to WebAssembly with
  [pygbag](https://pygame-web.github.io/) so it runs in the browser.
- **JavaScript** — a dependency-free single-file version.

## Play in the browser (Python, via WebAssembly)

**https://calap0309.github.io/snake-game/**

This is the real pygame game running in your browser — Python 3.12 compiled to
WASM by pygbag. Nothing to install.

## Run the Python version locally

```bash
python3 -m venv .venv
./.venv/bin/pip install pygame-ce
./.venv/bin/python pysnake/main.py
```

## Rebuild the web (WASM) version

```bash
./.venv/bin/pip install pygbag
./.venv/bin/pygbag --build pysnake
# output lands in pysnake/build/web/
```

## JavaScript version

Open `snake-js.html` in any browser, or visit
`https://calap0309.github.io/snake-game/snake-js.html`.

## Controls

- **Arrow keys / WASD** — move
- **P or Space** — pause / resume (also start)
- **R** — restart

Speed increases every 5 points.

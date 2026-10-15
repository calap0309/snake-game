# Snake 🐍

A tiny, dependency-free Snake game in a single HTML file.

## Play

Open `snake.html` in any modern browser — no build step, no server needed.

Or serve it locally:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/snake.html
```

## Controls

- **Arrow keys / WASD** — move
- **P or Space** — pause / resume
- **R** — restart
- **Swipe** — move on touch devices

Speed increases every 5 points. Best score is saved in `localStorage`.

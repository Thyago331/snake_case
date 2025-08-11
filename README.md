# snake_case

`snake_case` is an autonomous snake clicker game built with Pygame. Rather than controlling a single snake, you watch a colony of AI snakes roam a grid while you manage resources to spawn more.

## Features

- **Autonomous Snakes** – simple AI seeks food and avoids collisions.
- **Clicker Mechanics** – earn currency from snake actions and buy more snakes.
- **Persistent High Score** – stored in a per-user data directory via `platformdirs`.
- **Minimal Sound Effects** – small tones generated at runtime, no audio files shipped.
- **Speed Toggle** – switch between normal speed and a fast-forward mode.

## Project Structure

```
snake_case/
├── snake_case/
│   ├── audio/             # Sound generation utilities
│   ├── core/              # Game loop, constants and snake logic
│   ├── persistence/       # High score handling
│   ├── ui/                # Drawing helpers
│   ├── steam_integration.py  # Placeholder for Steamworks API
│   └── main.py            # Entry point
├── build_linux.sh         # PyInstaller helper script (Linux)
├── build_win.sh           # PyInstaller helper script (Windows)
├── pyproject.toml         # Project metadata and dependencies
├── requirements.txt       # Runtime dependencies
└── README.md
```

## Running from Source

```bash
pip install -r requirements.txt
python -m snake_case.main
```

## Building Executables

PyInstaller scripts are provided for Linux and Windows:

```bash
./build_linux.sh   # or build_win.sh on Windows
```

The scripts bundle the entry point into a single executable suitable for distribution platforms such as Steam.

## Audio Licensing

Sound effects are generated programmatically at runtime and are released into the public domain.

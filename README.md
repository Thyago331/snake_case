# snake_case

`snake_case` is a unique clicker-style game developed using the `gemini-cli` and Pygame. In this game, you don't directly control the snakes. Instead, you observe multiple autonomous snakes moving on a grid, eating food, and growing. Your role is to manage the game's economy by purchasing new snakes to increase your score and currency.

## Features

-   **Autonomous Snakes**: Snakes move independently, prioritizing food and avoiding collisions.
-   **Clicker Mechanics**: Earn currency as snakes eat and die, then use it to purchase more snakes.
-   **Dynamic Gameplay**: Snakes grow and slow down as they eat, adding a strategic element.
-   **Persistent High Score**: Your highest score is saved between game sessions.
-   **Sound Effects**: Immersive audio for background music, eating, and snake deaths.
-   **Speed Boost**: Toggle between normal and 10x speed for faster gameplay.

## Project Structure

The project is organized into a modular structure for better maintainability:

```
snake_case/
├── src/
│   ├── assets/             # Contains sound files (e.g., .mp3)
│   ├── constants.py        # Defines game constants, colors, and states
│   ├── game.py             # Manages overall game logic, states, and UI
│   ├── main.py             # The main entry point for the game
│   └── snake.py            # Implements the Snake class and its AI
├── dist/                   # Contains the generated executable (main.exe)
├── build/                  # PyInstaller build artifacts
├── main.spec               # PyInstaller specification file
├── requirements.txt        # Lists Python dependencies
└── README.md               # This file
```

## How to Run

### 1. Install Dependencies

First, ensure you have Python installed. Then, install the required libraries using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Run from Source

To run the game directly from the source code, navigate to the project's root directory and execute `main.py`:

```bash
python src/main.py
```

### 3. Run the Executable

A pre-built executable (`main.exe`) is available in the `dist/` directory. You can run this file directly without needing to install Python or any dependencies.

```bash
./dist/main.exe
```

## How to Build the Executable (for Developers)

If you make changes to the source code and want to generate a new executable, follow these steps:

1.  **Install PyInstaller** (if you haven't already):

    ```bash
    pip install pyinstaller
    ```

2.  **Rebuild the Executable**:

    Navigate to the project's root directory and run PyInstaller using the provided spec file:

    ```bash
    python -m PyInstaller --noconfirm --onefile --windowed --add-data "src/assets;assets" --add-data "highscore.txt;." src/main.py
    ```

    The new `main.exe` will be generated in the `dist/` folder.

## Development with `gemini-cli`

This project was interactively developed and refined using the `gemini-cli`. The `gemini-cli` facilitated tasks such as:

-   Initial project scaffolding.
-   Refactoring code into a modular structure.
-   Implementing game mechanics and features.
-   Debugging issues (e.g., sound, window closing).
-   Generating the executable for release.

Feel free to explore the commit history to see the iterative development process guided by the `gemini-cli`.

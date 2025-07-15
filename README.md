# Python 2048 AI Player

This project is a Python implementation of the classic 2048 game, complete with a graphical user interface (GUI) built using the Tkinter library. The main feature is a highly configurable AI bot that uses the **Expectimax algorithm** with advanced heuristics to play the game automatically.

## Features

- **Classic 2048 Gameplay**: A fully functional 4x4 grid game of 2048.
- **Interactive GUI**: A clean UI built with `tkinter` that includes game controls.
- **Advanced AI Player**: An intelligent bot that uses the Expectimax search algorithm coupled with powerful heuristics to make strategic decisions.
- **Full Game Control**:
    - **Start/Stop AI**: Toggle the AI on and off at any time with a button.
    - **Restart Game**: Instantly start a new game.
    - **Manual Play**: Play the game yourself using the arrow keys when the AI is stopped.
- **Configurable AI Depth**: Adjust the AI's search depth in real-time using a slider to balance between speed and intelligence.

## How It Works: The AI

The AI uses the **Expectimax algorithm**, a variation of Minimax designed for games with an element of chance. At its core, the AI "thinks" ahead for a certain number of moves (the "depth") to decide which action is best.

1.  **Maximizer (AI's Turn)**: The AI simulates each of the four possible moves (Up, Down, Left, Right).
2.  **Chance Node (Game's Turn)**: After each simulated move, the game adds a new tile ('2' or '4'). The AI calculates the *expected* outcome by averaging the scores of all possible random tile placements, weighted by their probability (90% for a '2', 10% for a '4').
3.  **Advanced Heuristic Evaluation**: To decide how "good" a board is, the AI uses a sophisticated evaluation function that scores the board based on four key heuristics:
    - **Smoothness**: Measures how similar adjacent tiles are. A "smooth" board with small differences between neighboring tiles gets a higher score because it's easier to merge.
    - **Monotonicity**: Rewards boards where tile values are generally increasing or decreasing along rows and columns. This encourages building chains and prevents high-value tiles from getting trapped.
    - **Empty Cells**: More empty cells mean more options. This heuristic is still crucial for maneuverability.
    - **Max Tile Value**: Gives a small bonus for creating higher-value tiles, directly encouraging progress.
4.  **Decision**: By looking ahead `N` steps (the configured depth), the AI chooses the move that leads to the state with the highest calculated heuristic score.

## Requirements

- Python 3.x
- Tkinter (usually included with standard Python installations)
- NumPy

You can install NumPy with pip:
```bash
pip install numpy
```

## How to Run

1.  Clone this repository or download the `2048_2.py` file.
2.  Open your terminal or command prompt.
3.  Navigate to the directory where the file is saved.
4.  Run the script with the following command:
    ```bash
    python 2048_2.py
    ```
The game window will appear, ready for you to play or start the AI.

### Using the Controls

- **Start AI / Stop AI Button**: Click this to have the AI take over. Click it again to pause the AI and regain manual control.
- **Restart Button**: Click to reset the board and start a new game.
- **AI Depth Slider**: Drag the slider to change the search depth of the Expectimax algorithm.
    - **Depth 1-2**: Fast but shortsighted. Good for seeing basic AI behavior.
    - **Depth 3**: A solid balance between speed and performance. The recommended default.
    - **Depth 4+**: Significantly smarter and more strategic, but each move will take longer to compute.
- **Arrow Keys**: When the AI is stopped, use the **Up, Down, Left, and Right arrow keys** to play manually.

## Code Structure

- **`Board` class**: Manages the core game logic, board state, and all Tkinter GUI elements. It's responsible for creating the window, grid, and control widgets, and for performing move operations (`move_up`, `compress_grid`, etc.).
- **`Game` class**: Orchestrates the game flow and contains all AI logic. It initializes the game, handles user input from buttons and keys, and runs the Expectimax algorithm (`expectimax`, `evaluate_grid`, `auto_move`).
- **Heuristic Weights**: Inside the `Game` class `__init__` method, you can find the weights for each heuristic (`WEIGHT_SMOOTH`, `WEIGHT_MONO`, etc.). Feel free to experiment by tuning these values to see how it changes the AI's playstyle!
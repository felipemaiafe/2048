# Python 2048 AI Player

This project is a Python implementation of the classic 2048 game, complete with a graphical user interface (GUI) built using the Tkinter library. The main feature is an AI bot that uses the **Expectimax algorithm** to play the game automatically, trying to achieve the highest score possible.

## Features

- **Classic 2048 Gameplay**: A fully functional 4x4 grid game of 2048.
- **Graphical User Interface**: A clean and simple UI built with Python's standard `tkinter` library.
- **AI Player**: An intelligent bot that decides the best move using the Expectimax search algorithm.
- **Dual Mode**: The script supports both AI-driven gameplay and manual control with the arrow keys.

## How It Works: The AI

The AI is the core of this project. It uses the **Expectimax algorithm**, a variation of Minimax designed for games with an element of chance.

1.  **Maximizer (Our Turn)**: The AI simulates each of the four possible moves (Up, Down, Left, Right). For each move, it looks ahead to see what the board state would become.
2.  **Chance Node (Computer's Turn)**: After the AI makes a move, the game randomly adds a new tile (a '2' or a '4') to an empty cell. The Expectimax algorithm accounts for this randomness by calculating the *expected* score over all possible random tile placements.
3.  **Evaluation**: The AI evaluates the "goodness" of a board state using a heuristic. In this implementation, the heuristic is simple: **it prioritizes moves that result in the maximum number of empty cells**. This encourages merges and keeps the board open for future moves.
4.  **Decision**: By looking ahead a few turns (a depth of 3 in the code), the AI chooses the move that leads to the best-expected outcome.

## Requirements

- Python 3.x
- Tkinter (usually included with standard Python installations)
- NumPy (imported in the script, though not actively used in the current version)

## How to Run

1.  Clone this repository or download the `2048_2.py` file.
2.  Open your terminal or command prompt.
3.  Navigate to the directory where the file is saved.
4.  Run the script with the following command:
    ```bash
    python 2048_2.py
    ```
The game window will appear, and the AI will automatically start playing after a 1-second delay.

### Playing Manually

The script is set up to run the AI by default. If you want to play manually, you can comment out one line of code.

1.  Open `2048_2.py` in a code editor.
2.  Go to the `start` method within the `Game` class.
3.  Find this line:
    ```python
    self.gamepanel.window.after(1000, self.auto_move)
    ```
4.  Comment it out by adding a `#` at the beginning:
    ```python
    # self.gamepanel.window.after(1000, self.auto_move)
    ```
5.  Save the file and run it again. You can now control the game with the **Up, Down, Left, and Right arrow keys**.

## Code Structure

- **`Board` class**: Manages the core game logic, including the 4x4 grid, move operations (`move_up`, `compressGrid`, etc.), and scorekeeping.
- **`GUIBoard` class**: Inherits from `Board` and handles all the Tkinter GUI elements. It is responsible for creating the window, grid cells, and updating the visuals.
- **`Game` class**: Orchestrates the game flow. It initializes the game, links keyboard inputs, and contains the AI's Expectimax logic (`expectimax`, `auto_move`).

## Possible Improvements

- **Better Heuristics**: The current evaluation function is very simple. A more advanced AI could be built using stronger heuristics, such as:
    - **Monotonicity**: Rewarding boards where tile values increase or decrease along rows and columns.
    - **Smoothness**: Rewarding boards where adjacent tiles have similar values.
    - **Corner Priority**: Encouraging the AI to keep the highest-value tile in a corner.
- **Adjustable AI Depth**: Add an option to change the search depth of the Expectimax algorithm to balance performance and intelligence.
- **UI Controls**: Add buttons to the GUI to start/stop the AI or restart the game.

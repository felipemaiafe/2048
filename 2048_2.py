from tkinter import *
from tkinter import messagebox
import random
import numpy as np

class Board:
    """
    Manages the core game logic and board state. This class does not handle the GUI.
    """
    bg_color={
        '2': '#eee4da', '4': '#ede0c8', '8': '#edc850', '16': '#edc53f',
        '32': '#f67c5f', '64': '#f65e3b', '128': '#edcf72', '256': '#edcc61',
        '512': '#f2b179', '1024': '#f59563', '2048': '#edc22e',
    }
    color={
        '2': '#776e65', '4': '#776e65', '8': '#f9f6f2', '16': '#f9f6f2',
        '32': '#f9f6f2', '64': '#f9f6f2', '128': '#f9f6f2', '256': '#f9f6f2',
        '512': '#f9f6f2', '1024': '#f9f6f2', '2048': '#f9f6f2',
    }

    def __init__(self):
        self.n = 4
        self.window = Tk()
        self.window.title('2048 AI Player')
        self.game_area = Frame(self.window, bg='azure3')
        
        self.grid_cells_ui = []
        for i in range(self.n):
            row_ui = []
            for j in range(self.n):
                l = Label(self.game_area, text='', bg='azure4', font=('arial', 22, 'bold'), width=4, height=2)
                l.grid(row=i, column=j, padx=7, pady=7)
                row_ui.append(l)
            self.grid_cells_ui.append(row_ui)
        self.game_area.grid()
        
        # Board state and logic variables
        self.grid_cell = [[0] * 4 for _ in range(4)]
        self.compress = False
        self.merge = False
        self.moved = False
        self.score = 0

    def reverse(self):
        for ind in range(self.n):
            i, j = 0, self.n - 1
            while i < j:
                self.grid_cell[ind][i], self.grid_cell[ind][j] = self.grid_cell[ind][j], self.grid_cell[ind][i]
                i += 1
                j -= 1

    def transpose(self):
        self.grid_cell = [list(t) for t in zip(*self.grid_cell)]

    def compress_grid(self):
        self.compress = False
        temp = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            cnt = 0
            for j in range(self.n):
                if self.grid_cell[i][j] != 0:
                    temp[i][cnt] = self.grid_cell[i][j]
                    if cnt != j:
                        self.compress = True
                    cnt += 1
        self.grid_cell = temp

    def merge_grid(self):
        self.merge = False
        for i in range(self.n):
            for j in range(self.n - 1):
                if self.grid_cell[i][j] == self.grid_cell[i][j + 1] and self.grid_cell[i][j] != 0:
                    self.grid_cell[i][j] *= 2
                    self.grid_cell[i][j + 1] = 0
                    self.score += self.grid_cell[i][j]
                    self.merge = True

    def random_cell(self):
        cells = []
        for i in range(self.n):
            for j in range(self.n):
                if self.grid_cell[i][j] == 0:
                    cells.append((i, j))
        if cells:
            curr = random.choice(cells)
            i, j = curr
            self.grid_cell[i][j] = 2 if random.random() < 0.9 else 4
    
    def can_merge(self):
        for i in range(self.n):
            for j in range(self.n - 1):
                if self.grid_cell[i][j] == self.grid_cell[i][j+1]:
                    return True
        for i in range(self.n - 1):
            for j in range(self.n):
                if self.grid_cell[i+1][j] == self.grid_cell[i][j]:
                    return True
        return False

    def paint_grid(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.grid_cell[i][j] == 0:
                    self.grid_cells_ui[i][j].config(text='', bg='azure4')
                else:
                    cell_text = str(self.grid_cell[i][j])
                    bg = self.bg_color.get(cell_text, '#3c3a32') # Default for high numbers
                    fg = self.color.get(cell_text, '#f9f6f2')   # Default for high numbers
                    self.grid_cells_ui[i][j].config(text=cell_text, bg=bg, fg=fg)
        self.window.update_idletasks() # Force UI update

    def move_up(self):
        self.transpose()
        self.compress_grid()
        self.merge_grid()
        self.moved = self.compress or self.merge
        self.compress_grid()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.reverse()
        self.compress_grid()
        self.merge_grid()
        self.moved = self.compress or self.merge
        self.compress_grid()
        self.reverse()
        self.transpose()

    def move_left(self):
        self.compress_grid()
        self.merge_grid()
        self.moved = self.compress or self.merge
        self.compress_grid()

    def move_right(self):
        self.reverse()
        self.compress_grid()
        self.merge_grid()
        self.moved = self.compress or self.merge
        self.compress_grid()
        self.reverse()

class Game:
    def __init__(self, board):
        self.board = board
        self.end = False
        self.won = False
        
        # --- AI and Control Attributes ---
        self.ai_running = False
        self.ai_after_id = None
        self.ai_depth = 3
        self.ai_move_delay = 100 # ms
        
        # --- Heuristic Weights ---
        self.WEIGHT_EMPTY = 2.7
        self.WEIGHT_SMOOTH = 0.1
        self.WEIGHT_MONO = 1.0
        self.WEIGHT_MAX_TILE = 1.0

    def start(self):
        self.add_ui_controls()
        self.board.random_cell()
        self.board.random_cell()
        self.board.paint_grid()
        self.board.window.bind('<Key>', self.link_keys)
        self.board.window.mainloop()
    
    def restart(self):
        # Stop AI if it's running
        if self.ai_running:
            self.toggle_ai()
            
        self.board.grid_cell = [[0] * 4 for _ in range(4)]
        self.board.score = 0
        self.end = False
        self.won = False
        self.board.random_cell()
        self.board.random_cell()
        self.board.paint_grid()
        
    def add_ui_controls(self):
        control_frame = Frame(self.board.window, bg='white')
        
        # Restart Button
        restart_button = Button(control_frame, text="Restart", command=self.restart)
        restart_button.pack(side=LEFT, padx=5, pady=5)
        
        # AI Toggle Button
        self.ai_toggle_button = Button(control_frame, text="Start AI", command=self.toggle_ai)
        self.ai_toggle_button.pack(side=LEFT, padx=5)
        
        # AI Depth Slider
        depth_label = Label(control_frame, text="AI Depth:", bg='white')
        depth_label.pack(side=LEFT, padx=(10, 0))
        self.depth_scale = Scale(control_frame, from_=1, to=5, orient=HORIZONTAL,
                                 command=lambda v: setattr(self, 'ai_depth', int(v)))
        self.depth_scale.set(self.ai_depth)
        self.depth_scale.pack(side=LEFT, padx=5)

        control_frame.grid(row=1, sticky='ew')

    def toggle_ai(self):
        self.ai_running = not self.ai_running
        if self.ai_running:
            self.ai_toggle_button.config(text="Stop AI")
            self.auto_move()
        else:
            self.ai_toggle_button.config(text="Start AI")
            if self.ai_after_id:
                self.board.window.after_cancel(self.ai_after_id)
                self.ai_after_id = None

    def link_keys(self, event):
        if self.end or self.won or self.ai_running:
            return

        self.board.compress = False
        self.board.merge = False
        self.board.moved = False

        key = event.keysym
        moves = {'Up': self.board.move_up, 'Down': self.board.move_down,
                 'Left': self.board.move_left, 'Right': self.board.move_right}
        
        if key in moves:
            moves[key]()
            if self.board.moved:
                self.board.random_cell()
                self.board.paint_grid()
                self.check_game_state()
    
    def check_game_state(self):
        if any(2048 in row for row in self.board.grid_cell):
            self.won = True
            messagebox.showinfo('2048', 'You Won!!')
            if self.ai_running: self.toggle_ai()
            return
            
        if not any(0 in row for row in self.board.grid_cell) and not self.board.can_merge():
            self.end = True
            messagebox.showinfo('2048', 'Game Over!!!')
            if self.ai_running: self.toggle_ai()

    def auto_move(self):
        if not self.ai_running or self.end or self.won:
            self.ai_toggle_button.config(text="Start AI")
            self.ai_running = False
            return
        
        _, best_move = self.expectimax(self.board.grid_cell, self.ai_depth, True)
        
        if best_move is None:
            self.check_game_state() # Triggers game over message
            return
        
        moves = {'Up': self.board.move_up, 'Down': self.board.move_down,
                 'Left': self.board.move_left, 'Right': self.board.move_right}
        
        if best_move in moves:
            moves[best_move]()
            if self.board.moved:
                self.board.random_cell()
            
        self.board.paint_grid()
        self.check_game_state()
        
        self.ai_after_id = self.board.window.after(self.ai_move_delay, self.auto_move)
    
    # --- AI Expectimax Logic ---

    def expectimax(self, grid, depth, is_max_player):
        if depth == 0 or self.is_game_over(grid):
            return self.evaluate_grid(grid), None

        if is_max_player:
            max_eval = float('-inf')
            best_move = None
            for move in ['Up', 'Down', 'Left', 'Right']:
                new_grid = self.simulate_move(grid, move)
                if new_grid == grid:
                    continue
                
                eval, _ = self.expectimax(new_grid, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else: # Chance player
            total_eval = 0
            empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
            num_empty = len(empty_cells)
            
            if num_empty == 0:
                return self.evaluate_grid(grid), None

            for cell in empty_cells:
                # Possibility of a 2 tile (90%)
                grid_with_2 = [row[:] for row in grid]
                grid_with_2[cell[0]][cell[1]] = 2
                eval_2, _ = self.expectimax(grid_with_2, depth - 1, True)
                total_eval += 0.9 * eval_2

                # Possibility of a 4 tile (10%)
                grid_with_4 = [row[:] for row in grid]
                grid_with_4[cell[0]][cell[1]] = 4
                eval_4, _ = self.expectimax(grid_with_4, depth - 1, True)
                total_eval += 0.1 * eval_4
            
            return total_eval / num_empty, None

    # --- Heuristic Evaluation ---

    def evaluate_grid(self, grid):
        """Calculates a heuristic score for a given grid state."""
        empty_cells = len([(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0])
        smoothness = self.calculate_smoothness(grid)
        monotonicity = self.calculate_monotonicity(grid)
        max_tile = np.max(grid)

        return (self.WEIGHT_EMPTY * np.log(empty_cells + 1) +
                self.WEIGHT_SMOOTH * smoothness +
                self.WEIGHT_MONO * monotonicity +
                self.WEIGHT_MAX_TILE * np.log2(max_tile + 1))
    
    def calculate_smoothness(self, grid):
        """Measures how close in value adjacent tiles are. Higher is better."""
        smoothness = 0
        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    val = np.log2(grid[i][j])
                    # Check right neighbor
                    if j < 3 and grid[i][j+1] != 0:
                        neighbor_val = np.log2(grid[i][j+1])
                        smoothness -= abs(val - neighbor_val)
                    # Check down neighbor
                    if i < 3 and grid[i+1][j] != 0:
                        neighbor_val = np.log2(grid[i+1][j])
                        smoothness -= abs(val - neighbor_val)
        return smoothness

    def calculate_monotonicity(self, grid):
        """Measures if values are generally increasing/decreasing along rows/cols."""
        mono_scores = [0, 0, 0, 0] # Up, Down, Left, Right
        
        # Left/Right
        for i in range(4):
            for j in range(3):
                if grid[i][j] != 0 and grid[i][j+1] != 0:
                    if grid[i][j] > grid[i][j+1]:
                        mono_scores[2] += np.log2(grid[i][j+1]) - np.log2(grid[i][j])
                    else:
                        mono_scores[3] += np.log2(grid[i][j]) - np.log2(grid[i][j+1])
        
        # Up/Down
        for j in range(4):
            for i in range(3):
                if grid[i][j] != 0 and grid[i+1][j] != 0:
                    if grid[i][j] > grid[i+1][j]:
                        mono_scores[0] += np.log2(grid[i+1][j]) - np.log2(grid[i][j])
                    else:
                        mono_scores[1] += np.log2(grid[i][j]) - np.log2(grid[i+1][j])
        
        return max(mono_scores[0], mono_scores[1]) + max(mono_scores[2], mono_scores[3])

    # --- Simulation and Game State Helpers ---

    def is_game_over(self, grid):
        if any(0 in row for row in grid):
            return False
        for i in range(4):
            for j in range(3):
                if grid[i][j] == grid[i][j+1] or grid[j][i] == grid[j+1][i]:
                    return False
        return True

    def simulate_move(self, grid, move):
        temp_board = [row[:] for row in grid]
        if move == 'Up':
            return self.move_up_sim(temp_board)
        elif move == 'Down':
            return self.move_down_sim(temp_board)
        elif move == 'Left':
            return self.move_left_sim(temp_board)
        elif move == 'Right':
            return self.move_right_sim(temp_board)
        return temp_board

    @staticmethod
    def _transpose(grid): return [list(row) for row in zip(*grid)]
    @staticmethod
    def _reverse(grid): return [row[::-1] for row in grid]

    @staticmethod
    def _compress(grid):
        new_grid = [[0] * 4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if grid[i][j] != 0:
                    new_grid[i][pos] = grid[i][j]
                    pos += 1
        return new_grid

    @staticmethod
    def _merge(grid):
        for i in range(4):
            for j in range(3):
                if grid[i][j] != 0 and grid[i][j] == grid[i][j+1]:
                    grid[i][j] *= 2
                    grid[i][j+1] = 0
        return grid

    def move_up_sim(self, grid):
        grid = self._transpose(grid)
        grid = self._compress(grid)
        grid = self._merge(grid)
        grid = self._compress(grid)
        return self._transpose(grid)

    def move_down_sim(self, grid):
        grid = self._transpose(grid)
        grid = self._reverse(grid)
        grid = self._compress(grid)
        grid = self._merge(grid)
        grid = self._compress(grid)
        grid = self._reverse(grid)
        return self._transpose(grid)

    def move_left_sim(self, grid):
        grid = self._compress(grid)
        grid = self._merge(grid)
        return self._compress(grid)

    def move_right_sim(self, grid):
        grid = self._reverse(grid)
        grid = self._compress(grid)
        grid = self._merge(grid)
        grid = self._compress(grid)
        return self._reverse(grid)

if __name__ == "__main__":
    board = Board()
    game = Game(board)
    game.start()
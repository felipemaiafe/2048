from tkinter import *
from tkinter import messagebox
import random
import numpy as np

class Board:
    bg_color={

        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#edc850',
        '16': '#edc53f',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#f2b179',
        '1024': '#f59563',
        '2048': '#edc22e',
    }
    color={
        '2': '#776e65',
        '4': '#f9f6f2',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#776e65',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }

    def __init__(self):
        self.n = 4
        self.gridCell = [[0] * 4 for _ in range(4)]
        self.compress = False
        self.merge = False
        self.moved = False
        self.score = 0

    def reverse(self):
        for ind in range(4):
            i = 0
            j = 3
            while i < j:
                self.gridCell[ind][i], self.gridCell[ind][j] = self.gridCell[ind][j], self.gridCell[ind][i]
                i += 1
                j -= 1

    def transpose(self):
        self.gridCell = [list(t) for t in zip(*self.gridCell)]

    def compressGrid(self):
        self.compress = False
        temp = [[0] * 4 for _ in range(4)]
        for i in range(4):
            cnt = 0
            for j in range(4):
                if self.gridCell[i][j] != 0:
                    temp[i][cnt] = self.gridCell[i][j]
                    if cnt != j:
                        self.compress = True
                    cnt += 1
        self.gridCell = temp

    def mergeGrid(self):
        self.merge = False
        for i in range(4):
            for j in range(4 - 1):
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j + 1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True

    def random_cell(self):
        cells = []
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    cells.append((i, j))
        if cells:
            curr = random.choice(cells)
            i, j = curr
            self.gridCell[i][j] = 2 if random.random() < 0.9 else 4
    
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
        for i in range(3):
            for j in range(4):
                if self.gridCell[i+1][j] == self.gridCell[i][j]:
                    return True
        return False

    def move_up(self):
        self.transpose()
        self.compressGrid()
        self.mergeGrid()
        self.moved = self.compress or self.merge
        self.compressGrid()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.reverse()
        self.compressGrid()
        self.mergeGrid()
        self.moved = self.compress or self.merge
        self.compressGrid()
        self.reverse()
        self.transpose()

    def move_left(self):
        self.compressGrid()
        self.mergeGrid()
        self.moved = self.compress or self.merge
        self.compressGrid()

    def move_right(self):
        self.reverse()
        self.compressGrid()
        self.mergeGrid()
        self.moved = self.compress or self.merge
        self.compressGrid()
        self.reverse()

class Game:
    def __init__(self, gamepanel):
        self.gamepanel = gamepanel
        self.end = False
        self.won = False

    def start(self):
        self.gamepanel.random_cell()
        self.gamepanel.random_cell()
        self.gamepanel.paintGrid()
        self.gamepanel.window.bind('<Key>', self.link_keys)
        self.gamepanel.window.after(1000, self.auto_move)
        self.gamepanel.window.mainloop()
    
    def link_keys(self, event):
        if self.end or self.won:
            return

        self.gamepanel.compress = False
        self.gamepanel.merge = False
        self.gamepanel.moved = False

        presed_key = event.keysym

        if presed_key == 'Up':
            self.gamepanel.move_up()
        elif presed_key == 'Down':
            self.gamepanel.move_down()
        elif presed_key == 'Left':
            self.gamepanel.move_left()
        elif presed_key == 'Right':
            self.gamepanel.move_right()
        else:
            return

        if self.gamepanel.moved:
            self.gamepanel.random_cell()
        
        self.gamepanel.paintGrid()
        print(self.gamepanel.score)

        flag = 0
        for i in range(4):
            for j in range(4):
                if self.gamepanel.gridCell[i][j] == 2048:
                    flag = 1
                    break

        if flag == 1: # found 2048
            self.won = True
            messagebox.showinfo('2048', message='You Won!!')
            print("won")
            return

        flag = 0
        for i in range(4):
            for j in range(4):
                if self.gamepanel.gridCell[i][j] == 0:
                    flag = 1
                    break

        if not (flag or self.gamepanel.can_merge()):
            self.end = True
            messagebox.showinfo('2048', 'Game Over!!!')
            print("Over")

    def auto_move(self):
        if self.end or self.won:
            return

        best_move = self.expectimax(self.gamepanel.gridCell, 3, True)[1]
        print(f"AI selected move: {best_move}")

        if best_move is None:
            messagebox.showinfo('2048', 'Game Over!!!')
            self.end = True
            return

        if best_move == 'Up':
            self.gamepanel.move_up()
        elif best_move == 'Down':
            self.gamepanel.move_down()
        elif best_move == 'Left':
            self.gamepanel.move_left()
        elif best_move == 'Right':
            self.gamepanel.move_right()

        if self.gamepanel.moved:
            self.gamepanel.random_cell()

        self.gamepanel.paintGrid()
        self.gamepanel.window.after(500, self.auto_move)

    def expectimax(self, grid, depth, is_max_player):
        if depth == 0 or self.is_game_over(grid):
            return self.evaluate(grid), None

        if is_max_player:
            max_eval = float('-inf')
            best_move = None
            for move in ['Up', 'Down', 'Left', 'Right']:
                new_grid = self.make_move(grid, move)
                if new_grid == grid:
                    continue
                eval = self.expectimax(new_grid, depth - 1, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            total_eval = 0
            empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
            num_empty = len(empty_cells)
            for cell in empty_cells:
                i, j = cell
                for value in [2, 4]:
                    new_grid = [row[:] for row in grid]
                    new_grid[i][j] = value
                    eval = self.expectimax(new_grid, depth - 1, True)[0]
                    total_eval += (0.9 if value == 2 else 0.1) * eval
            return total_eval / num_empty, None

    def make_move(self, grid, move):
        board_copy = [row[:] for row in grid]
        if move == 'Up':
            return self.move_up_sim(board_copy)
        elif move == 'Down':
            return self.move_down_sim(board_copy)
        elif move == 'Left':
            return self.move_left_sim(board_copy)
        elif move == 'Right':
            return self.move_right_sim(board_copy)
        return board_copy

    def move_up_sim(self, grid):
        grid = self.transpose(grid)
        grid = self.compress_grid(grid)
        grid = self.merge_grid(grid)
        grid = self.compress_grid(grid)
        grid = self.transpose(grid)
        return grid

    def move_down_sim(self, grid):
        grid = self.transpose(grid)
        grid = self.reverse(grid)
        grid = self.compress_grid(grid)
        grid = self.merge_grid(grid)
        grid = self.compress_grid(grid)
        grid = self.reverse(grid)
        grid = self.transpose(grid)
        return grid

    def move_left_sim(self, grid):
        grid = self.compress_grid(grid)
        grid = self.merge_grid(grid)
        grid = self.compress_grid(grid)
        return grid

    def move_right_sim(self, grid):
        grid = self.reverse(grid)
        grid = self.compress_grid(grid)
        grid = self.merge_grid(grid)
        grid = self.compress_grid(grid)
        grid = self.reverse(grid)
        return grid

    def transpose(self, grid):
        return [list(row) for row in zip(*grid)]

    def reverse(self, grid):
        return [row[::-1] for row in grid]

    def compress_grid(self, grid):
        new_grid = [[0] * 4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if grid[i][j] != 0:
                    new_grid[i][pos] = grid[i][j]
                    pos += 1
        return new_grid

    def merge_grid(self, grid):
        for i in range(4):
            for j in range(3):
                if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    grid[i][j + 1] = 0
        return grid

    def evaluate(self, grid):
        empty_cells = sum(row.count(0) for row in grid)
        return empty_cells

    def is_game_over(self, grid):
        for i in range(4):
            for j in range(4):
                if grid[i][j] == 0:
                    return False
                if i < 3 and grid[i][j] == grid[i + 1][j]:
                    return False
                if j < 3 and grid[i][j] == grid[i][j + 1]:
                    return False
        return True

class GUIBoard(Board):
    def __init__(self):
        super().__init__()
        self.window = Tk()
        self.window.title('2048 Game')
        self.gameArea = Frame(self.window, bg='azure3')
        self.board = []
        for i in range(4):
            rows = []
            for j in range(4):
                l = Label(self.gameArea, text='', bg='azure4', font=('arial', 22, 'bold'), width=4, height=2)
                l.grid(row=i, column=j, padx=7, pady=7)
                rows.append(l)
            self.board.append(rows)
        self.gameArea.grid()

    def paintGrid(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    self.board[i][j].config(text='', bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),
                                            bg=self.bg_color.get(str(self.gridCell[i][j])),
                                            fg=self.color.get(str(self.gridCell[i][j])))

gamepanel = GUIBoard()
game2048 = Game(gamepanel)
game2048.start()
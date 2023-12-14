import tkinter as tk
import random
import pickle
from tkinter import messagebox
from tkinter import filedialog
from abc import ABC, abstractmethod


class AbstractCell(ABC):
    def __init__(self, is_alive=False):
        self.is_alive = is_alive

    @abstractmethod
    def update(self, is_alive):
        pass


class AbstractCellFactory(ABC):
    @abstractmethod
    def create_cell(self, is_alive=False):
        pass


class Cell(AbstractCell):
    def update(self, is_alive):
        self.is_alive = is_alive


class CellFactory(AbstractCellFactory):
    def create_cell(self, is_alive=False):
        return Cell(is_alive)


class GameOfLife:
    def __init__(self, rows, cols, cell_factory):
        self.rows, self.cols = rows, cols
        self.grid = [[cell_factory.create_cell() for _ in range(cols)] for _ in range(rows)]

    def step(self):
        changes = [(i, j, False) if self.grid[i][j].is_alive and (live := self.count_live_neighbours(i, j)) not in {2, 3}
                   else (i, j, True) if not self.grid[i][j].is_alive and self.count_live_neighbours(i, j) == 3
                   else None
                   for i in range(self.rows) for j in range(self.cols)]

        for i, j, state in filter(None, changes):
            self.grid[i][j].update(state)

    def count_live_neighbours(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return sum(1 for dr, dc in directions if 0 <= (row + dr) < self.rows and 0 <= (c := col + dc) < self.cols and self.grid[row + dr][c].is_alive)

    def randomize(self):
        for row in self.grid:
            for cell in row:
                cell.is_alive = random.choice([True, False])


class GameOfLifeGUI:
    def __init__(self, root, rows, cols, cell_size=10):
        self.root, self.rows, self.cols, self.cell_size = root, rows, cols, cell_size
        self.game_running, self.game = False, GameOfLife(rows, cols, CellFactory())
        self.canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()
        self.start_button = tk.Button(root, text="Start", command=self.toggle_game_state)
        self.start_button.pack()
        self.draw_grid()
        self.game.randomize()
        self.update_canvas()

        self.save_button = tk.Button(root, text="Save", command=self.save_game)
        self.save_button.pack()
        self.load_button = tk.Button(root, text="Load", command=self.load_game)
        self.load_button.pack()

    def toggle_game_state(self):
        self.game_running = not self.game_running
        self.start_button.config(text="Stop" if self.game_running else "Start")
        self.run_game()

    def run_game(self):
        if self.game_running:
            self.game.step()
            self.update_canvas()
            self.root.after(100, self.run_game)

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1, x2, y2 = j * self.cell_size, i * self.cell_size, (j + 1) * self.cell_size, (i + 1) * self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray", tags=f"cell_{i}_{j}")
                self.canvas.tag_bind(f"cell_{i}_{j}", '<Button-1>', lambda event, i=i, j=j: self.toggle_cell(i, j))

    def update_canvas(self):
        for i in range(self.rows):
            for j in range(self.cols):
                color = "black" if self.game.grid[i][j].is_alive else "white"
                self.canvas.itemconfig(f"cell_{i}_{j}", fill=color)

    def toggle_cell(self, row, col):
        cell = self.game.grid[row][col]
        cell.update(not cell.is_alive)
        self.update_canvas()

    def save_game(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".gol", filetypes=[("Game of Life files", "*.gol"), ("All files", "*.*")])
        if not filepath:
            return

        try:
            with open(filepath, "wb") as file:
                pickle.dump([[cell.is_alive for cell in row] for row in self.game.grid], file)
            messagebox.showinfo("Save Game", "Successfully saved!")
        except Exception as e:
            messagebox.showerror("Save Game", f"An error occurred: {e}")

    def load_game(self):
        filepath = filedialog.askopenfilename(filetypes=[("Game of Life files", "*.gol"), ("All files", "*.*")])
        if not filepath:
            return

        try:
            with open(filepath, "rb") as file:
                grid_state = pickle.load(file)

            for i in range(self.rows):
                for j in range(self.cols):
                    self.game.grid[i][j].update(grid_state[i][j])
            self.update_canvas()
            messagebox.showinfo("Load Game", "Successfully loaded!")
        except Exception as e:
            messagebox.showerror("Load Game", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GameOfLifeGUI(root, 40, 40, 10)
    root.mainloop()

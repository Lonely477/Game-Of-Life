# Game-Of-Life
# Features
Game of Life Logic: Implements the core logic of Conway's Game of Life.
Graphical Interface: Uses Tkinter for a simple graphical user interface.
Start/Stop Button: Allows users to start and stop the simulation.
Save/Load Functionality: Enables users to save and load game states.

# Usage
Click the "Start" button to begin the simulation.
Click the "Stop" button to pause the simulation.
Toggle individual cells by clicking on them.
Save and load game states using the respective buttons.

## Cell (Abstract Base Class):

 ### Purpose: This is an abstract base class (ABC) representing a generic cell in the Game of Life.
 ### Attributes: is_alive: A boolean indicating whether the cell is alive or dead.
### Methods: update(self, is_alive): An abstract method to be implemented by subclasses. It updates the cell's state.

## BasicCell (Derived from Cell):

### Purpose: This class represents a basic implementation of a cell in the Game of Life.
### Methods:update(self, is_alive): Implements the abstract method from the base class to update the cell's state.

## GameOfLife:

### Purpose: This class represents the Game of Life simulation.
### Attributes:rows, cols: The number of rows and columns in the simulation grid.grid: A 2D list representing the grid of cells.

### Methods:__init__(self, rows, cols, cell_class): Initializes the game with a grid of cells of the specified class.step(self): Advances the simulation by one step according to the rules of the Game of Life.count_live_neighbours(self, row, col): Counts the number of live neighbors for a given cell.randomize(self): Randomizes the initial state of the grid.

## GameOfLifeGUI:

### Purpose: This class represents the graphical user interface for the Game of Life.
### Attributes:
#### root: The Tkinter root window.rows, 
#### cols: The number of rows and columns in the simulation 
#### grid.cell_size: The size of each cell in pixels 
#### game_running: A boolean indicating whether the game is currently 
#### running.game: An instance of the GameOfLife class.
#### canvas: The Tkinter canvas for displaying the grid.
### Methods:
#### __init__(self, root, rows, cols, cell_size): Initializes the GUI.
#### create_widgets(self): Creates buttons and sets up the canvas.
#### toggle_game_state(self): Toggles the game between running and paused states.
#### run_game(self): Runs the game in a loop if it's in the running state.
#### draw_grid(self): Draws the initial grid on the canvas.
#### update_canvas(self): Updates the canvas based on the current state of the grid.
#### toggle_cell(self, row, col): Toggles the state of a cell when clicked.
#### save_game(self): Saves the current game state to a file.
#### load_game(self): Loads a game state from a file.

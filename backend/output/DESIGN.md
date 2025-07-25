```markdown
# Minesweeper Game - Detailed Design

## Module: `main.py`

### Class: Application
The main class responsible for managing the game state, rendering the UI, and handling user interactions.

#### Methods:
- `__init__(self, grid_size: Tuple[int, int], mine_count: int) -> None`
  - Initializes the game with a grid of specified size and mine count.
  - Parameters:
    - `grid_size` - A tuple representing the dimensions of the grid (rows, columns).
    - `mine_count` - Integer representing the total number of mines on the board.

- `start_game(self) -> None`
  - Sets up the game, initializes the board, and places mines.

- `render(self) -> None`
  - Renders the game UI in the web browser, creating an interactive grid layout.

- `handle_left_click(self, row: int, col: int) -> None`
  - Handles the logic when a cell is left-clicked, revealing a cell or triggering a reveal.
  - Parameters:
    - `row` - Row index of the cell clicked.
    - `col` - Column index of the cell clicked.

- `handle_right_click(self, row: int, col: int) -> None`
  - Handles the logic when a cell is right-clicked, flagging or unflagging a mine.
  - Parameters:
    - `row` - Row index of the cell clicked.
    - `col` - Column index of the cell clicked.

- `recursive_reveal(self, row: int, col: int) -> None`
  - Reveals the cell at (row, col) and recursively reveals all adjacent cells if the cell is empty.

- `check_win(self) -> bool`
  - Checks whether the player has won (all non-mine cells revealed).
  - Returns:
    - True if the player has won, False otherwise.

- `check_loss(self) -> bool`
  - Checks whether the player has lost (clicked on a mine).
  - Returns:
    - True if the player has lost, False otherwise.

- `show_end_dialog(self, message: str) -> None`
  - Displays a modal dialog with the game's outcome message (win or loss).

- `restart_game(self) -> None`
  - Resets the game without changing the selected difficulty settings.

### Class: GameLogic
Handles all game logic related to the Minesweeper game such as grid setup, mine placement, and victory/loss conditions.

#### Methods:
- `__init__(self, grid_size: Tuple[int, int], mine_count: int) -> None`
  - Initializes the game logic with grid size and mine count.

- `generate_grid(self) -> List[List[Cell]]`
  - Generates a grid of the specified size and initializes cells.

- `place_mines(self) -> None`
  - Randomly places mines over the grid based on the mine count.

- `count_adjacent_mines(self) -> None`
  - Updates the cell count for adjacent mines for each cell after mines are placed.

- `is_safe_cell(self, row: int, col: int) -> bool`
  - Checks if a cell is safe to click (i.e., it does not contain a mine).

### Class: Cell
Represents a single cell in the Minesweeper grid.

#### Methods:
- `__init__(self, is_mine: bool) -> None`
  - Initializes the Cell.
  - Parameters:
    - `is_mine` - Boolean indicating if the cell is a mine.

- `reveal(self) -> None`
  - Reveals the cell.

- `flag(self) -> None`
  - Flags the cell as a mine.

- `unflag(self) -> None`
  - Unflags the cell.

- `is_revealed(self) -> bool`
  - Returns whether the cell is revealed.

- `is_flagged(self) -> bool`
  - Returns whether the cell is flagged.

### Class: UI
Handles the user interface rendering and interactions.

#### Methods:
- `__init__(self, application: Application) -> None`
  - Initializes the UI with a reference to the Application.

- `create_grid(self) -> None`
  - Creates the HTML elements for the grid of cells.

- `update_cell_display(self, row: int, col: int) -> None`
  - Updates the visual representation of a cell based on its state (revealed, mine, flagged).

- `show_modal(self, message: str) -> None`
  - Displays a modal window with a given message.

### Steps for Implementation:
1. **Setup the Environment**
   - Set up a Python environment and install any necessary web frameworks (such as Flask or Django).

2. **Create `main.py` File**
   - Start the development of the `main.py` module.

3. **Implement Application Class**
   - Implement the class to manage game state and rendering.
   - Create methods for starting the game, handling user input, and checking for win/loss conditions.

4. **Implement GameLogic Class**
   - Create logic for generating a grid of cells and placing mines.
   - Implement methods for counting adjacent mines and exposing cells recursively.

5. **Implement Cell Class**
   - Structure the `Cell` class to track whether a cell is a mine, revealed, or flagged.

6. **Implement UI Class**
   - Create the UI to visually represent the minesweeper game, create interactive elements, and manage user interactions via clicks.

7. **Connect Classes**
   - Ensure the `Application` class appropriately communicates with the `GameLogic`, `Cell`, and `UI` classes.

8. **Include Unit Tests**
   - Write unit tests for each class to validate the logic for grid generation, mine placement, and game state checks.

9. **Testing**
   - Thoroughly test the gameplay mechanics and responses to user inputs. Fix any bugs that arise during testing.

10. **Deployment**
    - Prepare for deployment or further integration with a web interface.
```
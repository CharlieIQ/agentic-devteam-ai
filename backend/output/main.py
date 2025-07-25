from typing import List, Tuple
import random

class Cell:
    def __init__(self, is_mine: bool) -> None:
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False

    def reveal(self) -> None:
        self.is_revealed = True

    def flag(self) -> None:
        self.is_flagged = True

    def unflag(self) -> None:
        self.is_flagged = False

    def is_revealed(self) -> bool:
        return self.is_revealed

    def is_flagged(self) -> bool:
        return self.is_flagged


class GameLogic:
    def __init__(self, grid_size: Tuple[int, int], mine_count: int) -> None:
        self.grid_size = grid_size
        self.mine_count = mine_count
        self.grid = self.generate_grid()

    def generate_grid(self) -> List[List[Cell]]:
        grid = [[Cell(False) for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        self.place_mines(grid)
        self.count_adjacent_mines(grid)
        return grid

    def place_mines(self, grid: List[List[Cell]]) -> None:
        mine_locations = set()
        while len(mine_locations) < self.mine_count:
            row = random.randint(0, self.grid_size[0] - 1)
            col = random.randint(0, self.grid_size[1] - 1)
            if (row, col) not in mine_locations:
                mine_locations.add((row, col))
                grid[row][col] = Cell(True)

    def count_adjacent_mines(self, grid: List[List[Cell]]) -> None:
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if grid[row][col].is_mine:
                    continue
                count = 0
                for r in range(max(0, row - 1), min(row + 2, self.grid_size[0])):
                    for c in range(max(0, col - 1), min(col + 2, self.grid_size[1])):
                        if grid[r][c].is_mine:
                            count += 1
                grid[row][col].adjacent_mines = count

    def is_safe_cell(self, row: int, col: int) -> bool:
        return not self.grid[row][col].is_mine


class Application:
    def __init__(self, grid_size: Tuple[int, int], mine_count: int) -> None:
        self.grid_size = grid_size
        self.mine_count = mine_count
        self.logic = GameLogic(grid_size, mine_count)
        self.game_over = False
        self.won = False

    def start_game(self) -> None:
        self.logic = GameLogic(self.grid_size, self.mine_count)
        self.game_over = False
        self.won = False
        self.render()

    def render(self) -> None:
        # Placeholder for rendering logic in a web browser
        pass
        
    def handle_left_click(self, row: int, col: int) -> None:
        if self.game_over or self.logic.grid[row][col].is_revealed:
            return
        
        self.logic.grid[row][col].reveal()
        if self.logic.grid[row][col].is_mine:
            self.game_over = True
            self.show_end_dialog("You hit a mine! Game Over!")
        else:
            if self.logic.grid[row][col].adjacent_mines == 0:
                self.recursive_reveal(row, col)
        
        if self.check_win():
            self.game_over = True
            self.show_end_dialog("Congratulations! You win!")

    def handle_right_click(self, row: int, col: int) -> None:
        if self.game_over or self.logic.grid[row][col].is_revealed:
            return
        
        if self.logic.grid[row][col].is_flagged:
            self.logic.grid[row][col].unflag()
        else:
            self.logic.grid[row][col].flag()
        
        self.render()

    def recursive_reveal(self, row: int, col: int) -> None:
        if not (0 <= row < self.grid_size[0]) or not (0 <= col < self.grid_size[1]):
            return
        if self.logic.grid[row][col].is_revealed or self.logic.grid[row][col].is_mine:
            return
        
        self.logic.grid[row][col].reveal()
        
        if self.logic.grid[row][col].adjacent_mines == 0:
            for r in range(max(0, row - 1), min(row + 2, self.grid_size[0])):
                for c in range(max(0, col - 1), min(col + 2, self.grid_size[1])):
                    self.recursive_reveal(r, c)

    def check_win(self) -> bool:
        for row in self.logic.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def show_end_dialog(self, message: str) -> None:
        # Placeholder for rendering end game dialog
        pass

    def restart_game(self) -> None:
        self.start_game()


class UI:
    def __init__(self, application: Application) -> None:
        self.application = application

    def create_grid(self) -> None:
        # Placeholder for creating HTML grid
        pass

    def update_cell_display(self, row: int, col: int) -> None:
        # Placeholder for updating cell display in the UI
        pass

    def show_modal(self, message: str) -> None:
        # Placeholder for showing modal in the UI
        pass
import unittest
from main import Application, Cell, GameLogic

class TestCell(unittest.TestCase):

    def test_initialize_cell(self):
        cell = Cell(is_mine=True)
        self.assertTrue(cell.is_mine)
        self.assertFalse(cell.is_revealed)
        self.assertFalse(cell.is_flagged)

    def test_reveal_cell(self):
        cell = Cell(is_mine=False)
        cell.reveal()
        self.assertTrue(cell.is_revealed)

    def test_flag_cell(self):
        cell = Cell(is_mine=False)
        cell.flag()
        self.assertTrue(cell.is_flagged)

    def test_unflag_cell(self):
        cell = Cell(is_mine=False)
        cell.flag()
        cell.unflag()
        self.assertFalse(cell.is_flagged)


class TestGameLogic(unittest.TestCase):

    def setUp(self):
        self.game_logic = GameLogic(grid_size=(3, 3), mine_count=1)

    def test_generate_grid_size(self):
        self.assertEqual(len(self.game_logic.grid), 3)
        self.assertEqual(len(self.game_logic.grid[0]), 3)

    def test_place_mines(self):
        mine_count = sum(cell.is_mine for row in self.game_logic.grid for cell in row)
        self.assertEqual(mine_count, 1)

    def test_adjacent_mine_count(self):
        self.assertTrue(hasattr(self.game_logic.grid[0][0], 'adjacent_mines'))

    def test_is_safe_cell(self):
        self.assertFalse(self.game_logic.is_safe_cell(0, 0))

        
class TestApplication(unittest.TestCase):

    def setUp(self):
        self.app = Application(grid_size=(3, 3), mine_count=1)

    def test_start_game(self):
        self.app.start_game()
        self.assertFalse(self.app.game_over)
        self.assertFalse(self.app.won)

    def test_handle_left_click_reveal_mine(self):
        self.app.start_game()
        for row in range(3):
            for col in range(3):
                if self.app.logic.grid[row][col].is_mine:
                    self.app.handle_left_click(row, col)
                    self.assertTrue(self.app.game_over)

    def test_handle_left_click_reveal_safe_cell(self):
        self.app.start_game()
        for row in range(3):
            for col in range(3):
                if not self.app.logic.grid[row][col].is_mine:
                    self.app.handle_left_click(row, col)
                    self.assertTrue(self.app.logic.grid[row][col].is_revealed)

    def test_check_win(self):
        self.app.start_game()
        for row in range(3):
            for col in range(3):
                if not self.app.logic.grid[row][col].is_mine:
                    self.app.logic.grid[row][col].reveal()
        self.assertTrue(self.app.check_win())    

if __name__ == '__main__':
    unittest.main()
import pygame
import random
import unittest
from unittest.mock import patch, MagicMock
from main import Application

class TestApplication(unittest.TestCase):

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.font.Font')
    def setUp(self, mock_font, mock_display, mock_init):
        self.app = Application()

    def test_initial_conditions(self):
        self.assertEqual(self.app.bird_y, 250)
        self.assertEqual(self.app.bird_velocity, 0)
        self.assertEqual(self.app.gravity, 0.5)
        self.assertFalse(self.app.game_over)
        self.assertEqual(self.app.score, 0)
        self.assertEqual(len(self.app.pipes), 1)

    def test_pipe_addition(self):
        initial_length = len(self.app.pipes)
        self.app.frame_counter = 100
        self.app.update()
        self.assertGreater(len(self.app.pipes), initial_length)

    def test_bird_falls_due_to_gravity(self):
        initial_bird_y = self.app.bird_y
        self.app.update()
        self.assertGreater(self.app.bird_y, initial_bird_y)

    def test_bird_collision_with_pipes(self):
        self.app.pipes = [{'x': 50, 'height': 300}]
        self.app.bird_y = 250  # Bird's position in the collision range
        self.assertTrue(self.app.check_collisions())

    def test_bird_passes_pipe(self):
        self.app.pipes = [{'x': -10, 'height': 300}]  # Off-screen pipe
        self.app.bird_y = 250
        self.assertFalse(self.app.check_collisions())
        self.assertEqual(self.app.score, 0)
        self.app.update()  # Pipe should be removed
        self.assertEqual(self.app.score, 1)

    def test_game_over_state(self):
        self.app.bird_y = 601  # Force bird to fall below screen
        self.app.update()
        self.assertTrue(self.app.game_over)

    def test_reset_game(self):
        self.app.game_over = True
        self.app.reset_game()
        self.assertFalse(self.app.game_over)
        self.assertEqual(self.app.score, 0)
        self.assertEqual(len(self.app.pipes), 1)
        self.assertEqual(self.app.bird_y, 250)

    def test_apply_punishment(self):
        self.app.apply_punishment()
        self.assertGreater(self.app.punishment_start_time, 0)

if __name__ == '__main__':
    unittest.main()
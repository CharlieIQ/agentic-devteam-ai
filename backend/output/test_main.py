import unittest
from main import Application

class TestApplication(unittest.TestCase):

    def setUp(self):
        self.app = Application()

    def test_initial_step_goal(self):
        self.assertEqual(self.app.step_goal, 10000)

    def test_set_step_goal_valid(self):
        self.app.set_step_goal(15000)
        self.assertEqual(self.app.step_goal, 15000)

    def test_set_step_goal_invalid(self):
        with self.assertRaises(ValueError) as context:
            self.app.set_step_goal(0)
        self.assertTrue('Step goal must be greater than 0.' in str(context.exception))

    def test_log_steps_valid(self):
        self.app.log_steps(5000)
        self.assertEqual(self.app.total_steps, 5000)

    def test_log_steps_invalid(self):
        with self.assertRaises(ValueError) as context:
            self.app.log_steps(-500)
        self.assertTrue('Steps cannot be negative.' in str(context.exception))

    def test_check_progress_not_met(self):
        self.app.log_steps(5000)
        message = self.app.check_progress()
        self.assertIn("Wow, did you even get out of bed today?", message)

    def test_check_progress_met(self):
        self.app.log_steps(15000)
        message = self.app.check_progress()
        self.assertIn("Amazing! You've crushed your goal! 🎉", message)

    def test_save_daily_steps(self):
        self.app.log_steps(12000)
        self.app.save_daily_steps("2023-10-01")
        self.assertEqual(self.app.get_step_history(), {"2023-10-01": 12000})
        self.assertEqual(self.app.total_steps, 0)

    def test_get_step_history(self):
        self.app.log_steps(10000)
        self.app.save_daily_steps("2023-10-01")
        self.app.log_steps(8000)
        self.app.save_daily_steps("2023-10-02")
        history = self.app.get_step_history()
        self.assertEqual(history, {
            "2023-10-01": 10000,
            "2023-10-02": 8000
        })

if __name__ == '__main__':
    unittest.main()
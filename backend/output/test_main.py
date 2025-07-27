import unittest
from main import Application

class TestApplication(unittest.TestCase):

    def setUp(self):
        self.app = Application()

    def test_add_task(self):
        self.app.add_task("Finish homework by Friday")
        self.assertEqual(len(self.app.tasks), 1)
        self.assertEqual(self.app.tasks[0]['name'], "Finish homework")
        self.assertEqual(self.app.tasks[0]['deadline'], "Friday")

    def test_parse_task_description(self):
        task = self.app._parse_task_description("Read chapter 5 by Monday")
        self.assertEqual(task['name'], "Read chapter 5")
        self.assertEqual(task['deadline'], "Monday")

        task = self.app._parse_task_description("Just a random task")
        self.assertEqual(task['name'], "Just a random task")
        self.assertIsNone(task['deadline'])

    def test_suggest_schedule(self):
        self.app.add_task("Read the book by Saturday")
        self.app.add_task("Submit assignment by Friday")
        schedule = self.app.suggest_schedule()

        self.assertEqual(len(schedule), 2)
        self.assertEqual(schedule[0]['task'], "Read the book")
        self.assertEqual(schedule[1]['task'], "Submit assignment")

    def test_track_productivity(self):
        self.app.add_task("Task 1")
        self.app.track_productivity()
        self.assertIn("2023-", self.app.productivity_trends)

    def test_update_task_progress(self):
        self.app.add_task("Task 1")
        self.app.update_task_progress("Task 1", "completed")
        self.assertEqual(self.app.tasks[0]['status'], "completed")

    def test_burnout_detection(self):
        self.app.add_task("Task " + str(i) for i in range(6))
        with self.assertLogs() as log:
            self.app.check_burnout()
        self.assertIn("You have a heavy workload. Consider taking a break!", log.output[0])

if __name__ == '__main__':
    unittest.main()
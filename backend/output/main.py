import random

class Application:
    def __init__(self):
        self.step_goal = 10000  # Default daily step goal
        self.total_steps = 0
        self.history = {}  # Dictionary to keep history of steps with dates

    def set_step_goal(self, goal: int) -> None:
        """
        Set a new daily step goal.
        
        :param goal: The step goal to be set
        """
        if goal <= 0:
            raise ValueError("Step goal must be greater than 0.")
        self.step_goal = goal
    
    def log_steps(self, steps: int) -> None:
        """
        Log the steps taken in a day.
        
        :param steps: Number of steps to log
        """
        if steps < 0:
            raise ValueError("Steps cannot be negative.")
        
        self.total_steps += steps
    
    def check_progress(self) -> str:
        """
        Check progress against the daily goal and return appropriate messages.
        
        :return: A string message about progress
        """
        if self.total_steps < self.step_goal:
            return self._get_roast_message()
        else:
            return self._get_celebration_message()
    
    def _get_roast_message(self) -> str:
        """
        Generate a sarcastic remark if the user has not met the step goal.
        
        :return: A roast message
        """
        roasts = [
            "Wow, did you even get out of bed today?",
            "You call that exercise?",
            "I've seen sloths move faster!",
            "Was that a walk or just a slow shuffle?",
            "I'm starting to think you're part of the furniture."
        ]
        return random.choice(roasts)
    
    def _get_celebration_message(self) -> str:
        """
        Generate a celebratory message if the user has met/exceeded the step goal.
        
        :return: A celebration message
        """
        celebrations = [
            "Amazing! You've crushed your goal! 🎉",
            "You're a walking legend! Go show off!",
            "Did you just save the world by walking? Because it feels like it! 🌟",
            "Confetti for you! You're unstoppable!"
        ]
        return random.choice(celebrations)
    
    def save_daily_steps(self, date: str) -> None:
        """
        Save the total steps for the day along with the date.
        
        :param date: The date in yyyy-mm-dd format
        """
        self.history[date] = self.total_steps
        # Reset steps for the next day
        self.total_steps = 0
        
    def get_step_history(self) -> dict:
        """
        Retrieve history of daily steps.
        
        :return: A dictionary with dates and corresponding steps
        """
        return self.history
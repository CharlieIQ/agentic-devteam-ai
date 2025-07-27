```markdown
# Intelligent Student Planner App

The Intelligent Student Planner App is designed to help students manage their assignments, deadlines, and overall productivity while also monitoring their mental well-being. The app incorporates AI to create adaptive study schedules, integrates with Google Calendar, parses course syllabi from PDFs, and provides a natural language interface for adding tasks. The app includes features like Pomodoro timers, focus mode, and burn-out detection.

## Features

- **Task Management**: Track assignments, deadlines, and exams.
- **AI-Powered Scheduling**: Automatically suggest daily study schedules based on workload, deadlines, and productivity trends.
- **Integration**: Connects with Google Calendar and learning platforms such as Moodle.
- **Focus Mode**: Implements Pomodoro sessions and motivational nudges.
- **Natural Language Processing**: Add tasks using phrases like ‘Finish comp sci paper by Friday’.
- **AI Coach**: Dynamically adjusts schedules based on student progress.
- **Burnout Detection**: Suggests breaks when the workload becomes overwhelming.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
  - [Application](#application)
  - [CalendarIntegration](#calendarintegration)
  - [PDFParser](#pdfparser)
  - [LearningPlatformIntegration](#learningplatformintegration)
  - [FocusMode](#focusmode)
  - [AICoach](#aicoach)
  - [BurnoutDetector](#burnoutdetector)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.x
- Flask (for backend server)
- Axios (for making HTTP requests from front end)
- React (for frontend)
- PyPDF2 (for PDF parsing)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/intelligent-student-planner.git
   cd intelligent-student-planner
   ```

2. **Set up the backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up the frontend:**
   ```bash
   cd frontend
   npm install
   ```

4. **Run the backend server:**
   ```bash
   cd backend
   python app.py
   ```

5. **Run the frontend application:**
   ```bash
   cd frontend
   npm start
   ```

## Usage

To use the Intelligent Student Planner app, simply add your tasks using the input field, and the app will automatically suggest a study schedule based on your upcoming deadlines.

## API Documentation

### Application

The `Application` class manages tasks, deadlines, and schedules.

#### Methods

- **add_task(task_description: str)**: Adds a new task based on natural language input.
- **suggest_schedule()**: Generates a daily study schedule using AI.
- **track_productivity()**: Updates productivity trends.
- **enable_focus_mode()**: Activates focus mode features.
- **update_task_progress(task_name: str, status: str)**: Updates the status of a specific task.
- **check_burnout()**: Analyzes workload for burnout detection.

### CalendarIntegration

Handles Google Calendar interactions.

#### Methods

- **sync_events()**: Sync events from Google Calendar.
- **add_event(event_data: dict)**: Adds events to Google Calendar.

### PDFParser

Parses PDF syllabi for course information.

#### Methods

- **parse_syllabus(pdf_file_path: str)**: Extracts deadlines and assignments from a PDF syllabus.

### LearningPlatformIntegration

Integrates with learning platforms.

#### Methods

- **fetch_assignments()**: Fetches course assignments.

### FocusMode

Implements features to enhance concentration.

#### Methods

- **start_pomodoro()**: Starts a Pomodoro timer.

### AICoach

Provides AI-driven coaching.

#### Methods

- **adjust_plan(tasks: list)**: Adjusts plans based on task status.

### BurnoutDetector

Monitors user workload.

#### Methods

- **analyze_workload(tasks: list)**: Suggests breaks based on workload analysis.

## Examples

### Adding a Task

To add a task, use the input box as follows:
```
Finish comp sci paper by Friday
```

### Suggested Schedule

After tasks are added, the app will suggest a schedule similar to:

```
1. Finish comp sci paper at 2 PM
2. Study for Mathematics at 3 PM
```

### Checking Burnout

To check for burnout, the app will analyze current tasks and provide feedback:
```
You have a heavy workload. Consider taking a break!
```

## Contributing

We welcome contributions to the Intelligent Student Planner App. Please fork the repository and submit a pull request if you have enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
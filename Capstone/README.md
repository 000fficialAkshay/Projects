# Learning Tracker

Learning Tracker is a Django-based web application designed to help users organize courses, plan daily learning tasks, track study time, and monitor learning progress.

The application focuses on self-paced learning and accountability. Users decide what they want to study, how many tasks they want to commit to, and how much time they plan to spend.

## Features

### User Authentication
- User registration and login
- User logout
- User-specific courses, tasks, daily tasks, history, and statistics

### Dashboard
The dashboard provides an overview of current learning activity:
- Today's learning commitment
- Today's tasks
- Planned study time
- Actual study time
- Consistency calendar
- Most recently completed task

### Courses
Users can create and manage their own courses.

The course hierarchy is:

```text
Course
    └── Part
          └── Task
```

Users can add, edit, and delete courses, parts, and tasks.

### Course Progress
Each course displays a completion percentage based on its completed parts.

Parts can be marked as completed. When all parts in a course are completed, the course is automatically considered completed.

A responsive progress bar displays the completion percentage.

### Daily Tasks
Users can select tasks for their daily learning commitment.

Each `DailyTask` stores:
- User
- Task
- Date
- Planned minutes
- Actual time
- Completion status

The application uses daily commitments instead of automatically generating a long-term schedule, helping prevent unfinished tasks from creating a large future backlog.

### Task Timer
Each daily task has its own timer.

Users can:
1. Start a task timer.
2. Stop the timer.
3. Continue the timer later.
4. Complete the task.

Actual elapsed time is persisted in the database, so refreshing or leaving the page does not reset previously recorded time.

JavaScript handles the timer on the client side, while Django saves the recorded time.

### Planned vs Actual Time
The application records both planned and actual study time, allowing users to compare their original commitment with the time actually spent.

### Task Completion and History
Completed daily tasks are not deleted. Their completion state is stored and they are moved out of the current dashboard task list into History.

History records can show:
- Task name
- Completion date
- Planned time
- Actual time

A completed task can also be reverted if it was completed accidentally. Reverting returns it to an incomplete state.

### Consistency Calendar
The dashboard contains a calendar that visually highlights days with completed learning activity.

### Recent Results
The dashboard displays the latest completed task so the user can immediately see their most recent learning result.

### Statistics
The Statistics section provides longer-term learning information, including:
- Planned study time
- Actual study time
- Daily learning activity
- Completed tasks
- Daily consistency
- Highest number of tasks completed in a day

## Data Model

The main conceptual structure is:

```text
User
 │
 ├── Course
 │      │
 │      └── Part
 │             │
 │             └── Task
 │
 └── DailyTask
          │
          └── Task
```

A `DailyTask` represents a particular scheduled occurrence of a reusable `Task`.

Its main fields are:

```text
user
task
date
planned_minutes
actual_seconds
completed
```

`actual_seconds` allows accurate timer persistence while the interface can display the value as hours and minutes when appropriate.

## Technologies Used

### Backend
- Python
- Django
- Django ORM
- SQLite

### Frontend
- HTML
- CSS
- JavaScript

### Development Tools
- Git
- GitHub
- Django development server
- Browser Developer Tools

## JavaScript

JavaScript provides the application's interactive functionality, especially the daily-task timer.

It is responsible for:
- Starting and stopping timers
- Tracking elapsed seconds
- Associating timers with individual `DailyTask` records
- Sending recorded time to Django
- Updating the displayed timer
- Handling task-completion interactions
- Supporting interactive UI behavior

The timer is associated with `DailyTask` rather than the underlying `Task` because the same task can be scheduled on different dates.

## Responsive Design

The application is designed for both desktop and mobile screens.

The desktop interface uses a sidebar for navigation. On smaller screens, the navigation can be presented as a mobile menu.

Responsive behavior includes:
- Dashboard cards adapting to smaller screens
- Calendar cells adapting to available width
- Responsive course progress bars
- Fluid authentication fields
- Responsive course and history cards
- Prevention of unnecessary horizontal overflow

## Project Structure

A simplified Django structure is:

```text
project/
│
├── manage.py
│
├── tracker/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   │   └── tracker/
│   │       ├── layout.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── dashboard.html
│   │       ├── courses.html
│   │       ├── history.html
│   │       └── statistics.html
│   │
│   └── static/
│       └── tracker/
│           ├── dashboard.css
│           └── ...
│
└── ...
```

The exact structure may contain additional Django configuration, migration, JavaScript, and static files.

## Database

Django's ORM is used for database operations such as:
- Creating users
- Creating courses, parts, and tasks
- Creating daily task records
- Updating timer information
- Marking tasks as completed
- Reverting completed tasks
- Calculating course completion
- Retrieving history
- Calculating statistics

Django migrations manage changes to the database schema.

## How to Run

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create an administrator account if required:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Then open the local development server in a browser.

## Design Decisions

### User-controlled learning pace

Learning Tracker does not automatically decide how much the user should study.

The user decides:
- Which course to work on
- Which tasks to complete
- How many tasks to commit to
- How much time to allocate to each task

### Daily rather than long-term scheduling

The application focuses on daily commitments rather than automatically generating a long-term timetable. This helps prevent unfinished tasks from continuously accumulating in future schedules.

### Preserve completed records

Completed tasks remain in the database instead of being deleted. This makes it possible to maintain a history and generate statistics from previous learning activity.

### DailyTask instead of Task for timing

The timer records time against `DailyTask` rather than directly against `Task`. This separates a reusable learning task from a particular scheduled occurrence of that task.

## Future Improvements

Possible future improvements include:
- More detailed statistical charts
- Weekly and monthly study summaries
- More advanced streak calculations
- Study-time goals
- Course-specific statistics
- Exporting learning history
- More detailed task performance analysis
- Accessibility improvements
- Production deployment

## Conclusion

Learning Tracker combines course organization, daily learning commitments, time tracking, completion history, and progress monitoring in one Django application.

The project demonstrates Django models and relationships, authentication, database persistence, JavaScript interaction, asynchronous requests, HTML templates, CSS responsive design, and user-focused application design.

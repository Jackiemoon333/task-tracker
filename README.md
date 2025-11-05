# Task Tracker CLI

A multi-language command-line task tracker application built for learning purposes. Supports Python (with SQLite), JavaScript (Node.js), and Go implementations.

## Features

- ✅ Add, update, and delete tasks
- ✅ Mark tasks as todo, in-progress, or done
- ✅ List all tasks with filtering by status
- ✅ List completed tasks
- ✅ List pending tasks (todo + in-progress)
- ✅ List tasks in progress
- ✅ Beautiful colored terminal output
- ✅ Multiple database backends (JSON, SQLite)

## Installation

### Python Version (Recommended)

The Python version uses SQLite for persistent storage and includes full CRUD operations.

```bash
# Install dependencies
pip install -r requirements.txt

# Or with python3
python3 -m pip install -r requirements.txt
```

**Requirements:**
- Python 3.7+
- click==8.1.7
- colorama==0.4.6

### JavaScript/Node.js Version

```bash
# No dependencies needed - uses Node.js built-in modules
node task-tracker.js add "My first task"
```

**Requirements:**
- Node.js 12+

### Go Version

```bash
# Compile and run
go run task-tracker.go add "My first task"

# Or build a binary
go build task-tracker.go
./task-tracker add "My first task"
```

**Requirements:**
- Go 1.16+

## Usage

### Python Version (SQLite)

```bash
# Add a task
python3 task_tracker_sqlite.py add "Learn Python SQLite"

# List all tasks
python3 task_tracker_sqlite.py list

# List tasks by status
python3 task_tracker_sqlite.py list --status done

# Update a task
python3 task_tracker_sqlite.py update 1 --status in-progress
python3 task_tracker_sqlite.py update 1 --title "New title"

# Delete a task
python3 task_tracker_sqlite.py delete 1
python3 task_tracker_sqlite.py delete 1 --yes  # Skip confirmation

# List completed tasks
python3 task_tracker_sqlite.py done

# List pending tasks
python3 task_tracker_sqlite.py pending

# List in-progress tasks
python3 task_tracker_sqlite.py in-progress
```

### Python Version (JSON - Legacy)

```bash
python3 task_tracker.py add "My task"
python3 task_tracker.py list
```

### JavaScript Version

```bash
# Add a task
node task-tracker.js add "Learn JavaScript"

# List all tasks
node task-tracker.js list

# List tasks by status
node task-tracker.js list done

# Show help
node task-tracker.js help
```

### Go Version

```bash
# Add a task
go run task-tracker.go add "Learn Go"

# List all tasks
go run task-tracker.go list

# List tasks by status
go run task-tracker.go list done

# Show help
go run task-tracker.go help
```

## Project Structure

```
to-do-tracker/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── task_tracker_sqlite.py       # Python version with SQLite (recommended)
├── task_tracker.py              # Python version with JSON storage
├── task-tracker.js              # JavaScript/Node.js version
├── task-tracker.go              # Go version
├── tasks.db                     # SQLite database (created automatically)
└── tasks.json                    # JSON storage (created automatically)
```

## Database Schema (SQLite)

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'todo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Learning Objectives

This project demonstrates:

- **CLI Development**: Building command-line interfaces
- **Data Persistence**: JSON files vs SQLite databases
- **Multi-language Development**: Same application in Python, JavaScript, and Go
- **Database Operations**: CRUD operations with SQL
- **Error Handling**: Graceful error management
- **User Experience**: Colored output, confirmation prompts, help systems

## Technology Comparison

### Python
- **Pros**: Easy to learn, rich ecosystem, great for data science/ML
- **Cons**: Slower than compiled languages
- **Best for**: Rapid prototyping, data analysis, ML applications

### JavaScript/Node.js
- **Pros**: Web integration, large ecosystem, async-friendly
- **Cons**: Single-threaded, dynamic typing can cause bugs
- **Best for**: Web applications, APIs, full-stack development

### Go
- **Pros**: Fast, compiled, great concurrency, single binary
- **Cons**: More verbose, steeper learning curve
- **Best for**: Backend services, system tools, high-performance applications

## Contributing

This is a learning project! Feel free to:
- Add new features
- Improve error handling
- Add more language implementations
- Enhance the UI/UX
- Add tests

## License

This project is open source and available for educational purposes.

## Author

Built as a learning project to explore:
- CLI development
- Database integration
- Multi-language programming
- Software architecture


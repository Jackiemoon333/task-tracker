#!/usr/bin/env python3
"""
Task Tracker CLI with SQLite Database - A learning project
"""

import click
import sqlite3
import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Global variable for our database file
DB_FILE = "tasks.db"

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_database():
    """Initialize the database and create tables if they don't exist"""
    conn = get_db_connection()
    
    # Create tasks table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'todo',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def load_tasks():
    """Load all tasks from database"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM tasks ORDER BY id')
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tasks

def save_task(title, status='todo'):
    """Save a new task to database"""
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO tasks (title, status) VALUES (?, ?)',
        (title, status)
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def update_task(task_id, title=None, status=None):
    """Update an existing task"""
    conn = get_db_connection()
    
    updates = []
    params = []
    
    if title is not None:
        updates.append('title = ?')
        params.append(title)
    
    if status is not None:
        updates.append('status = ?')
        params.append(status)
    
    if updates:
        updates.append('updated_at = CURRENT_TIMESTAMP')
        params.append(task_id)
        
        query = f'UPDATE tasks SET {", ".join(updates)} WHERE id = ?'
        cursor = conn.execute(query, params)
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        return rows_affected > 0
    
    conn.close()
    return False

def delete_task(task_id):
    """Delete a task from database"""
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def get_task_by_id(task_id):
    """Get a specific task by ID"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return dict(task) if task else None

@click.group() #Creates a group of commands
def cli():
    """Task Tracker with SQLite - Manage your tasks from the terminal"""
    # Initialize database on startup
    init_database()
    pass

@cli.command() #Creates a command
@click.argument('task_description') #Creates an argument for the command
def add(task_description):
    """Add a new task"""
    task_id = save_task(task_description)
    click.echo(f"{Fore.GREEN}✅ Added task #{task_id}: {Style.BRIGHT}{task_description}")

@cli.command() #Creates a command
@click.option('--status', type=click.Choice(['todo', 'in-progress', 'done']), help='Filter by status') #Optional filter
def list(status):
    """List all tasks, optionally filter by status"""
    if status:
        # Filter by status using SQL
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM tasks WHERE status = ? ORDER BY id', (status,))
        tasks = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not tasks:
            click.echo(f"{Fore.YELLOW}📋 No {status} tasks found!")
            return
        click.echo(f"{Fore.CYAN}📋 Your {status} tasks:")
    else:
        tasks = load_tasks()
        
        if not tasks:
            click.echo(f"{Fore.YELLOW}📋 No tasks yet! Add one with: {Style.BRIGHT}python task_tracker_sqlite.py add \"your task\"")
            return
        click.echo(f"{Fore.CYAN}📋 Your tasks:")
    
    for task in tasks:
        status_emoji = {
            'todo': '⏳',
            'in-progress': '🔄', 
            'done': '✅'
        }.get(task['status'], '❓')
        
        # Color code by status
        status_color = {
            'todo': Fore.YELLOW,
            'in-progress': Fore.BLUE,
            'done': Fore.GREEN
        }.get(task['status'], Fore.WHITE)
        
        click.echo(f"  {status_emoji} {Fore.WHITE}#{task['id']}: {Style.BRIGHT}{task['title']} {status_color}({task['status']})")

@cli.command() #Creates a command
@click.argument('task_id', type=int) #Converts argument to integer
@click.option('--title', help='New title for the task') #Optional parameter
@click.option('--status', type=click.Choice(['todo', 'in-progress', 'done']), help='New status for the task') #Choice validation
def update(task_id, title, status):
    """Update a task's title or status"""
    # Check if task exists
    existing_task = get_task_by_id(task_id)
    if not existing_task:
        click.echo(f"{Fore.RED}❌ Task #{task_id} not found!")
        return
    
    # Update fields if provided
    if title:
        click.echo(f"📝 Updated title: {title}")
    
    if status:
        click.echo(f"🔄 Updated status: {status}")
    
    if not title and not status:
        click.echo(f"{Fore.RED}❌ Please provide --title or --status to update")
        return
    
    success = update_task(task_id, title, status)
    if success:
        click.echo(f"{Fore.GREEN}✅ Task #{task_id} updated!")
    else:
        click.echo(f"{Fore.RED}❌ Failed to update task #{task_id}")

@cli.command() #Creates a command
@click.argument('task_id', type=int) #Converts argument to integer
@click.option('--yes', is_flag=True, help='Skip confirmation prompt') #Boolean flag
def delete(task_id, yes):
    """Delete a task"""
    # Check if task exists
    existing_task = get_task_by_id(task_id)
    if not existing_task:
        click.echo(f"{Fore.RED}❌ Task #{task_id} not found!")
        return
    
    # Confirmation prompt (unless --yes flag is used)
    if not yes:
        if not click.confirm(f"🗑️  Delete task #{task_id}: '{existing_task['title']}'?"):
            click.echo(f"{Fore.RED}❌ Deletion cancelled")
            return
    
    # Delete the task
    success = delete_task(task_id)
    if success:
        click.echo(f"{Fore.GREEN}✅ Task #{task_id} deleted!")
    else:
        click.echo(f"{Fore.RED}❌ Failed to delete task #{task_id}")

@cli.command() #Creates a command
def done():
    """List all completed tasks"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM tasks WHERE status = ? ORDER BY id', ('done',))
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not tasks:
        click.echo(f"{Fore.YELLOW}✅ No completed tasks yet!")
        return
    
    click.echo(f"{Fore.GREEN}✅ Completed tasks:")
    for task in tasks:
        click.echo(f"  ✅ {Fore.WHITE}#{task['id']}: {Style.BRIGHT}{task['title']}")

@cli.command() #Creates a command  
def pending():
    """List all pending tasks (todo + in-progress)"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM tasks WHERE status IN (?, ?) ORDER BY id', ('todo', 'in-progress'))
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not tasks:
        click.echo(f"{Fore.YELLOW}📋 No pending tasks! Great job!")
        return
    
    click.echo(f"{Fore.CYAN}📋 Pending tasks:")
    for task in tasks:
        status_emoji = {
            'todo': '⏳',
            'in-progress': '🔄'
        }.get(task['status'], '❓')
        
        click.echo(f"  {status_emoji} {Fore.WHITE}#{task['id']}: {Style.BRIGHT}{task['title']} {Fore.YELLOW}({task['status']})")

@cli.command() #Creates a command
def in_progress():
    """List all tasks currently in progress"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM tasks WHERE status = ? ORDER BY id', ('in-progress',))
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not tasks:
        click.echo(f"{Fore.YELLOW}🔄 No tasks in progress!")
        return
    
    click.echo(f"{Fore.BLUE}🔄 Tasks in progress:")
    for task in tasks:
        click.echo(f"  🔄 {Fore.WHITE}#{task['id']}: {Style.BRIGHT}{task['title']}")

if __name__ == '__main__': #Runs the CLI
    cli()


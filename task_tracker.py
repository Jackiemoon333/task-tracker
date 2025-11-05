#!/usr/bin/env python3
"""
Simple task tracker CLI - A learning project
"""

import click
import json
import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Global variable for our data file
DATA_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file, return empty list if file doesn't exist"""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def get_next_id(tasks):
    """Get the next available ID for a new task"""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

@click.group() #Creates a group of commands
def cli():
    """Task Tracker - Manage your tasks from the terminal"""
    pass

@cli.command() #Creates a command
@click.argument('task_description') #Creates an argument for the command
def add(task_description):
    """Add a new task"""
    tasks = load_tasks()
    
    new_task = {
        'id': get_next_id(tasks),
        'title': task_description,
        'status': 'todo',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    
    click.echo(f"{Fore.GREEN}✅ Added task #{new_task['id']}: {Style.BRIGHT}{task_description}")

@cli.command() #Creates a command
@click.option('--status', type=click.Choice(['todo', 'in-progress', 'done']), help='Filter by status') #Optional filter
def list(status):
    """List all tasks, optionally filter by status"""
    tasks = load_tasks()
    
    if not tasks:
        click.echo(f"{Fore.YELLOW}📋 No tasks yet! Add one with: {Style.BRIGHT}python task_tracker.py add \"your task\"")
        return
    
    # Filter tasks if status specified
    if status:
        tasks = [task for task in tasks if task['status'] == status]
        if not tasks:
            click.echo(f"{Fore.YELLOW}📋 No {status} tasks found!")
            return
        click.echo(f"{Fore.CYAN}📋 Your {status} tasks:")
    else:
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
def done():
    """List all completed tasks"""
    tasks = load_tasks()
    done_tasks = [task for task in tasks if task['status'] == 'done']
    
    if not done_tasks:
        click.echo("✅ No completed tasks yet!")
        return
    
    click.echo("✅ Completed tasks:")
    for task in done_tasks:
        click.echo(f"  ✅ #{task['id']}: {task['title']}")

@cli.command() #Creates a command  
def pending():
    """List all pending tasks (todo + in-progress)"""
    tasks = load_tasks()
    pending_tasks = [task for task in tasks if task['status'] in ['todo', 'in-progress']]
    
    if not pending_tasks:
        click.echo("📋 No pending tasks! Great job!")
        return
    
    click.echo("📋 Pending tasks:")
    for task in pending_tasks:
        status_emoji = {
            'todo': '⏳',
            'in-progress': '🔄'
        }.get(task['status'], '❓')
        
        click.echo(f"  {status_emoji} #{task['id']}: {task['title']} ({task['status']})")

@cli.command() #Creates a command
def in_progress():
    """List all tasks currently in progress"""
    tasks = load_tasks()
    in_progress_tasks = [task for task in tasks if task['status'] == 'in-progress']
    
    if not in_progress_tasks:
        click.echo("🔄 No tasks in progress!")
        return
    
    click.echo("🔄 Tasks in progress:")
    for task in in_progress_tasks:
        click.echo(f"  🔄 #{task['id']}: {task['title']}")

@cli.command() #Creates a command
@click.argument('task_id', type=int) #Converts argument to integer
@click.option('--title', help='New title for the task') #Optional parameter
@click.option('--status', type=click.Choice(['todo', 'in-progress', 'done']), help='New status for the task') #Choice validation

def update(task_id, title, status):
    """Update a task's title or status"""
    tasks = load_tasks()
    
    # Find the task by ID
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        click.echo(f"❌ Task #{task_id} not found!")
        return
    
    # Update fields if provided
    if title:
        task['title'] = title
        click.echo(f"📝 Updated title: {title}")
    
    if status:
        task['status'] = status
        click.echo(f"🔄 Updated status: {status}")
    
    if not title and not status:
        click.echo("❌ Please provide --title or --status to update")
        return
    
    save_tasks(tasks)
    click.echo(f"✅ Task #{task_id} updated!")

@cli.command() #Creates a command
@click.argument('task_id', type=int) #Converts argument to integer
@click.option('--yes', is_flag=True, help='Skip confirmation prompt') #Boolean flag
def delete(task_id, yes):
    """Delete a task"""
    tasks = load_tasks()
    
    # Find the task by ID
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        click.echo(f"❌ Task #{task_id} not found!")
        return
    
    # Confirmation prompt (unless --yes flag is used)
    if not yes:
        if not click.confirm(f"🗑️  Delete task #{task_id}: '{task['title']}'?"):
            click.echo("❌ Deletion cancelled")
            return
    
    # Remove the task
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    click.echo(f"✅ Task #{task_id} deleted!")

if __name__ == '__main__': #Runs the CLI
    cli()

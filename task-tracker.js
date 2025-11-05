#!/usr/bin/env node
/**
 * Task Tracker CLI - JavaScript/Node.js Version
 * Run with: node task-tracker.js
 */

const fs = require('fs');
const path = require('path');

const DATA_FILE = 'tasks.json';

// Colors for terminal output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    white: '\x1b[37m'
};

function loadTasks() {
    try {
        if (!fs.existsSync(DATA_FILE)) {
            return [];
        }
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        return [];
    }
}

function saveTasks(tasks) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(tasks, null, 2));
}

function getNextId(tasks) {
    if (tasks.length === 0) return 1;
    return Math.max(...tasks.map(task => task.id)) + 1;
}

function addTask(description) {
    const tasks = loadTasks();
    const newTask = {
        id: getNextId(tasks),
        title: description,
        status: 'todo',
        created_at: new Date().toISOString().slice(0, 19).replace('T', ' ')
    };
    
    tasks.push(newTask);
    saveTasks(tasks);
    
    console.log(`${colors.green}✅ Added task #${newTask.id}: ${colors.bright}${description}`);
}

function listTasks(statusFilter = null) {
    let tasks = loadTasks();
    
    if (tasks.length === 0) {
        console.log(`${colors.yellow}📋 No tasks yet! Add one with: ${colors.bright}node task-tracker.js add "your task"`);
        return;
    }
    
    if (statusFilter) {
        tasks = tasks.filter(task => task.status === statusFilter);
        if (tasks.length === 0) {
            console.log(`${colors.yellow}📋 No ${statusFilter} tasks found!`);
            return;
        }
        console.log(`${colors.cyan}📋 Your ${statusFilter} tasks:`);
    } else {
        console.log(`${colors.cyan}📋 Your tasks:`);
    }
    
    tasks.forEach(task => {
        const emoji = {
            'todo': '⏳',
            'in-progress': '🔄',
            'done': '✅'
        }[task.status] || '❓';
        
        const statusColor = {
            'todo': colors.yellow,
            'in-progress': colors.blue,
            'done': colors.green
        }[task.status] || colors.white;
        
        console.log(`  ${emoji} ${colors.white}#${task.id}: ${colors.bright}${task.title} ${statusColor}(${task.status})`);
    });
}

// Command line interface
const command = process.argv[2];
const arg = process.argv[3];

switch (command) {
    case 'add':
        if (!arg) {
            console.log(`${colors.red}❌ Please provide a task description`);
            process.exit(1);
        }
        addTask(arg);
        break;
        
    case 'list':
        listTasks(arg);
        break;
        
    case 'help':
    case '--help':
        console.log(`
${colors.cyan}Task Tracker - JavaScript Version${colors.reset}

Usage: node task-tracker.js <command> [arguments]

Commands:
  add <description>    Add a new task
  list [status]        List all tasks, optionally filter by status
  help                 Show this help message

Examples:
  node task-tracker.js add "Learn JavaScript"
  node task-tracker.js list
  node task-tracker.js list done
        `);
        break;
        
    default:
        console.log(`${colors.red}❌ Unknown command: ${command}`);
        console.log(`Use 'node task-tracker.js help' for usage information`);
        process.exit(1);
}

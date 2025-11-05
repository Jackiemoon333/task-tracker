package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

// Task represents a single task
type Task struct {
	ID        int    `json:"id"`
	Title     string `json:"title"`
	Status    string `json:"status"`
	CreatedAt string `json:"created_at"`
}

// Colors for terminal output
const (
	ColorReset  = "\033[0m"
	ColorBright = "\033[1m"
	ColorRed    = "\033[31m"
	ColorGreen  = "\033[32m"
	ColorYellow = "\033[33m"
	ColorBlue   = "\033[34m"
	ColorCyan   = "\033[36m"
	ColorWhite  = "\033[37m"
)

const dataFile = "tasks.json"

// loadTasks loads tasks from JSON file
func loadTasks() []Task {
	if _, err := os.Stat(dataFile); os.IsNotExist(err) {
		return []Task{}
	}

	data, err := ioutil.ReadFile(dataFile)
	if err != nil {
		return []Task{}
	}

	var tasks []Task
	if err := json.Unmarshal(data, &tasks); err != nil {
		return []Task{}
	}

	return tasks
}

// saveTasks saves tasks to JSON file
func saveTasks(tasks []Task) error {
	data, err := json.MarshalIndent(tasks, "", "  ")
	if err != nil {
		return err
	}

	return ioutil.WriteFile(dataFile, data, 0644)
}

// getNextID returns the next available ID
func getNextID(tasks []Task) int {
	if len(tasks) == 0 {
		return 1
	}

	maxID := 0
	for _, task := range tasks {
		if task.ID > maxID {
			maxID = task.ID
		}
	}
	return maxID + 1
}

// addTask adds a new task
func addTask(title string) {
	tasks := loadTasks()
	newTask := Task{
		ID:        getNextID(tasks),
		Title:     title,
		Status:    "todo",
		CreatedAt: time.Now().Format("2006-01-02 15:04:05"),
	}

	tasks = append(tasks, newTask)
	saveTasks(tasks)

	fmt.Printf("%s✅ Added task #%d: %s%s%s\n", 
		ColorGreen, newTask.ID, ColorBright, title, ColorReset)
}

// listTasks lists all tasks, optionally filtered by status
func listTasks(statusFilter string) {
	tasks := loadTasks()

	if len(tasks) == 0 {
		fmt.Printf("%s📋 No tasks yet! Add one with: %sgo run task-tracker.go add \"your task\"%s\n",
			ColorYellow, ColorBright, ColorReset)
		return
	}

	// Filter tasks if status specified
	if statusFilter != "" {
		var filteredTasks []Task
		for _, task := range tasks {
			if task.Status == statusFilter {
				filteredTasks = append(filteredTasks, task)
			}
		}
		tasks = filteredTasks

		if len(tasks) == 0 {
			fmt.Printf("%s📋 No %s tasks found!%s\n", ColorYellow, statusFilter, ColorReset)
			return
		}
		fmt.Printf("%s📋 Your %s tasks:%s\n", ColorCyan, statusFilter, ColorReset)
	} else {
		fmt.Printf("%s📋 Your tasks:%s\n", ColorCyan, ColorReset)
	}

	// Sort tasks by ID for consistent display
	sort.Slice(tasks, func(i, j int) bool {
		return tasks[i].ID < tasks[j].ID
	})

	for _, task := range tasks {
		emoji := "❓"
		statusColor := ColorWhite

		switch task.Status {
		case "todo":
			emoji = "⏳"
			statusColor = ColorYellow
		case "in-progress":
			emoji = "🔄"
			statusColor = ColorBlue
		case "done":
			emoji = "✅"
			statusColor = ColorGreen
		}

		fmt.Printf("  %s %s#%d: %s%s%s %s(%s)%s\n",
			emoji, ColorWhite, task.ID, ColorBright, task.Title, ColorReset,
			statusColor, task.Status, ColorReset)
	}
}

// showHelp displays help information
func showHelp() {
	fmt.Printf(`
%sTask Tracker - Go Version%s

Usage: go run task-tracker.go <command> [arguments]

Commands:
  add <description>    Add a new task
  list [status]        List all tasks, optionally filter by status
  help                 Show this help message

Examples:
  go run task-tracker.go add "Learn Go"
  go run task-tracker.go list
  go run task-tracker.go list done
`, ColorCyan, ColorReset)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Printf("%s❌ No command provided%s\n", ColorRed, ColorReset)
		showHelp()
		os.Exit(1)
	}

	command := os.Args[1]

	switch command {
	case "add":
		if len(os.Args) < 3 {
			fmt.Printf("%s❌ Please provide a task description%s\n", ColorRed, ColorReset)
			os.Exit(1)
		}
		title := strings.Join(os.Args[2:], " ")
		addTask(title)

	case "list":
		statusFilter := ""
		if len(os.Args) > 2 {
			statusFilter = os.Args[2]
		}
		listTasks(statusFilter)

	case "help", "--help":
		showHelp()

	default:
		fmt.Printf("%s❌ Unknown command: %s%s\n", ColorRed, command, ColorReset)
		showHelp()
		os.Exit(1)
	}
}

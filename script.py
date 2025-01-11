import time
import sqlite3
import datetime
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from plyer import notification
from datetime import timedelta
import calendar
import json

class ProductivityTracker:
    def __init__(self):
        """Initialize the productivity tracking system"""
        self.db_connection = sqlite3.connect('productivity.db')
        self.cursor = self.db_connection.cursor()
        self.create_tables()
        self.pomodoro_active = False
        self.current_task = None
        self.break_duration = 5  # Default break duration in minutes
        self.pomodoro_duration = 25  # Default pomodoro duration in minutes
        self.daily_goals = {}
        self.load_settings()
        self.setup_gui()

    def create_tables(self):
        """Create necessary database tables"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                created_at TIMESTAMP,
                completed_at TIMESTAMP,
                mood_score INTEGER,
                focus_score INTEGER,
                pomodoros_completed INTEGER,
                category TEXT,
                priority INTEGER,
                tags TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_tracking (
                id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP,
                mood_score INTEGER,
                energy_level INTEGER,
                stress_level INTEGER,
                notes TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_goals (
                id INTEGER PRIMARY KEY,
                date DATE,
                goal_type TEXT,
                target_value INTEGER,
                achieved_value INTEGER
            )
        ''')
        
        self.db_connection.commit()

    def setup_gui(self):
        """Setup the GUI interface with enhanced features"""
        self.root = tk.Tk()
        self.root.title("Productivity & Wellness Tracker Pro")
        self.root.geometry("1000x800")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Main task tab
        self.task_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.task_frame, text='Tasks')
        
        # Stats tab
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text='Analytics')
        
        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text='Settings')
        
        self._setup_task_tab()
        self._setup_stats_tab()
        self._setup_settings_tab()
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Timer display
        self.timer_label = tk.Label(self.task_frame, text="25:00", font=('Arial', 24))
        self.timer_label.pack(pady=10)

    def _setup_task_tab(self):
        """Setup the main task management interface"""
        # Task Entry Frame
        entry_frame = ttk.LabelFrame(self.task_frame, text="New Task")
        entry_frame.pack(fill='x', padx=5, pady=5)
        
        # Task details
        tk.Label(entry_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = tk.Entry(entry_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(entry_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_combo = ttk.Combobox(entry_frame, values=['Work', 'Study', 'Personal', 'Health'])
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(entry_frame, text="Priority:").grid(row=1, column=0, padx=5, pady=5)
        self.priority_combo = ttk.Combobox(entry_frame, values=['High', 'Medium', 'Low'])
        self.priority_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(entry_frame, text="Tags:").grid(row=1, column=2, padx=5, pady=5)
        self.tags_entry = tk.Entry(entry_frame, width=20)
        self.tags_entry.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(entry_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = tk.Text(entry_frame, height=3, width=60)
        self.desc_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        
        # Mood and Energy Tracking
        tracking_frame = ttk.LabelFrame(self.task_frame, text="Wellness Tracking")
        tracking_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(tracking_frame, text="Mood:").grid(row=0, column=0, padx=5, pady=5)
        self.mood_scale = tk.Scale(tracking_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.mood_scale.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(tracking_frame, text="Energy:").grid(row=0, column=2, padx=5, pady=5)
        self.energy_scale = tk.Scale(tracking_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.energy_scale.grid(row=0, column=3, padx=5, pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(self.task_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Start Task", command=self.start_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Start Pomodoro", command=self.start_pomodoro).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Complete Task", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        
        # Task List with Treeview
        self.task_tree = ttk.Treeview(self.task_frame, columns=('Title', 'Category', 'Priority', 'Created', 'Status'))
        self.task_tree.heading('Title', text='Title')
        self.task_tree.heading('Category', text='Category')
        self.task_tree.heading('Priority', text='Priority')
        self.task_tree.heading('Created', text='Created')
        self.task_tree.heading('Status', text='Status')
        self.task_tree.pack(fill='both', expand=True, padx=5, pady=5)

    def _setup_stats_tab(self):
        """Setup the statistics and analytics interface"""
        # Statistics controls
        control_frame = ttk.Frame(self.stats_frame)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(control_frame, text="Daily Overview", 
                  command=lambda: self.show_statistics('daily')).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Weekly Trends", 
                  command=lambda: self.show_statistics('weekly')).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Category Analysis", 
                  command=lambda: self.show_statistics('category')).pack(side=tk.LEFT, padx=5)
        
        # Placeholder for charts
        self.chart_frame = ttk.Frame(self.stats_frame)
        self.chart_frame.pack(fill='both', expand=True, padx=5, pady=5)

    def _setup_settings_tab(self):
        """Setup the settings interface"""
        settings_frame = ttk.LabelFrame(self.settings_frame, text="Preferences")
        settings_frame.pack(fill='x', padx=5, pady=5)
        
        # Pomodoro settings
        tk.Label(settings_frame, text="Pomodoro Duration (minutes):").grid(row=0, column=0, padx=5, pady=5)
        self.pomodoro_spinbox = ttk.Spinbox(settings_frame, from_=1, to=60, width=5)
        self.pomodoro_spinbox.set(self.pomodoro_duration)
        self.pomodoro_spinbox.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(settings_frame, text="Break Duration (minutes):").grid(row=1, column=0, padx=5, pady=5)
        self.break_spinbox = ttk.Spinbox(settings_frame, from_=1, to=30, width=5)
        self.break_spinbox.set(self.break_duration)
        self.break_spinbox.grid(row=1, column=1, padx=5, pady=5)
        
        # Daily goals
        goals_frame = ttk.LabelFrame(self.settings_frame, text="Daily Goals")
        goals_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(goals_frame, text="Tasks to Complete:").grid(row=0, column=0, padx=5, pady=5)
        self.daily_tasks_goal = ttk.Spinbox(goals_frame, from_=1, to=20, width=5)
        self.daily_tasks_goal.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(goals_frame, text="Pomodoros to Complete:").grid(row=1, column=0, padx=5, pady=5)
        self.daily_pomodoros_goal = ttk.Spinbox(goals_frame, from_=1, to=20, width=5)
        self.daily_pomodoros_goal.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.settings_frame, text="Save Settings", 
                  command=self.save_settings).pack(pady=10)

    def save_settings(self):
        """Save user preferences"""
        self.pomodoro_duration = int(self.pomodoro_spinbox.get())
        self.break_duration = int(self.break_spinbox.get())
        self.daily_goals = {
            'tasks': int(self.daily_tasks_goal.get()),
            'pomodoros': int(self.daily_pomodoros_goal.get())
        }
        with open('settings.json', 'w') as f:
            json.dump({
                'pomodoro_duration': self.pomodoro_duration,
                'break_duration': self.break_duration,
                'daily_goals': self.daily_goals
            }, f)
        messagebox.showinfo("Success", "Settings saved successfully!")

    def load_settings(self):
        """Load saved settings"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.pomodoro_duration = settings.get('pomodoro_duration', 25)
                self.break_duration = settings.get('break_duration', 5)
                self.daily_goals = settings.get('daily_goals', {'tasks': 5, 'pomodoros': 8})
        except FileNotFoundError:
            pass

    def start_task(self):
        """Start a new task with enhanced tracking"""
        title = self.task_entry.get()
        description = self.desc_entry.get("1.0", tk.END).strip()
        category = self.category_combo.get()
        priority = self.priority_combo.get()
        tags = self.tags_entry.get()
        mood = self.mood_scale.get()
        energy = self.energy_scale.get()

        if title:
            self.cursor.execute('''
                INSERT INTO tasks (
                    title, description, created_at, mood_score, 
                    pomodoros_completed, category, priority, tags
                )
                VALUES (?, ?, ?, ?, 0, ?, ?, ?)
            ''', (title, description, datetime.datetime.now(), mood, category, priority, tags))
            
            self.cursor.execute('''
                INSERT INTO mood_tracking (
                    timestamp, mood_score, energy_level, notes
                )
                VALUES (?, ?, ?, ?)
            ''', (datetime.datetime.now(), mood, energy, f"Task start: {title}"))
            
            self.db_connection.commit()
            self.update_task_list()
            self._clear_entry_fields()
            self.status_bar.config(text=f"Task '{title}' started")

    def complete_task(self):
        """Mark the selected task as complete"""
        selection = self.task_tree.selection()
        if selection:
            task_id = selection[0]
            self.cursor.execute('''
                UPDATE tasks 
                SET completed_at = ?
                WHERE id = ?
            ''', (datetime.datetime.now(), task_id))
            self.db_connection.commit()
            self.update_task_list()
            self._check_daily_goals()

    def _check_daily_goals(self):
        """Check and update progress towards daily goals"""
        today = datetime.date.today()
        
        # Check completed tasks
        self.cursor.execute('''
            SELECT COUNT(*) FROM tasks 
            WHERE DATE(completed_at) = DATE(?)
        ''', (today,))
        completed_tasks = self.cursor.fetchone()[0]
        
        if completed_tasks >= self.daily_goals.get('tasks', 5):
            notification.notify(
                title="Daily Goal Achieved!",
                message="You've reached your daily task completion goal!",
                timeout=10
            )

    def show_statistics(self, view_type='daily'):
        """Display enhanced productivity statistics"""
        plt.close('all')  # Clear any existing plots
        
        if view_type == 'daily':
            self._show_daily_stats()
        elif view_type == 'weekly':
            self._show_weekly_stats()
        elif view_type == 'category':
            self._show_category_stats()

    def _show_daily_stats(self):
        """Show daily productivity metrics"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Mood and energy trends
        self.cursor.execute('''
            SELECT DATE(timestamp), AVG(mood_score), AVG(energy_level)
            FROM mood_tracking
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
            LIMIT 7
        ''')
        data = self.cursor.fetchall


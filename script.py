import time
import sqlite3
import datetime
import threading
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from plyer import notification

class ProductivityTracker:
    def __init__(self):
        """Initialize the productivity tracking system"""
        self.db_connection = sqlite3.connect('productivity.db')
        self.cursor = self.db_connection.cursor()
        self.create_tables()
        self.pomodoro_active = False
        self.current_task = None
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
                pomodoros_completed INTEGER
            )
        ''')
self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_tracking (
                id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP,
                mood_score INTEGER,
                notes TEXT
            )
        ''')
        self.db_connection.commit()

def setup_gui(self):
        """Setup the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Productivity & Wellness Tracker")
        self.root.geometry("800x600")
# Task Entry
        tk.Label(self.root, text="Task Title:").pack()
        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.pack()

        tk.Label(self.root, text="Description:").pack()
        self.desc_entry = tk.Text(self.root, height=3, width=50)
        self.desc_entry.pack()

        # Mood Tracking
        tk.Label(self.root, text="Current Mood (1-10):").pack()
        self.mood_scale = tk.Scale(self.root, from_=1, to=10, orient=tk.HORIZONTAL)
        self.mood_scale.pack()

        # Buttons
        tk.Button(self.root, text="Start Task", command=self.start_task).pack()
        tk.Button(self.root, text="Start Pomodoro", command=self.start_pomodoro).pack()
        tk.Button(self.root, text="View Statistics", command=self.show_statistics).pack()

        # Task List
        self.task_listbox = tk.Listbox(self.root, width=50, height=10)
        self.task_listbox.pack()
        self.update_task_list()
    def start_task(self):
        """Start a new task with mood tracking"""
        title = self.task_entry.get()
        description = self.desc_entry.get("1.0", tk.END)
        mood = self.mood_scale.get()

        if title:
            self.cursor.execute('''
                INSERT INTO tasks (title, description, created_at, mood_score, pomodoros_completed)
                VALUES (?, ?, ?, ?, 0)
            ''', (title, description, datetime.datetime.now(), mood))
            self.db_connection.commit()
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
            self.desc_entry.delete("1.0", tk.END)

    def start_pomodoro(self):
        """Start a pomodoro timer"""
        if not self.pomodoro_active:
            self.pomodoro_active = True
            threading.Thread(target=self.pomodoro_timer).start()
def pomodoro_timer(self, duration=25):
        """Run a pomodoro timer"""
        minutes = duration
        while minutes > 0 and self.pomodoro_active:
            time.sleep(60)
            minutes -= 1

        if self.pomodoro_active:
            self.pomodoro_active = False
            notification.notify(
                title="Pomodoro Complete!",
                message="Time for a break!",
                timeout=10
            )
            self.update_pomodoro_count()
        


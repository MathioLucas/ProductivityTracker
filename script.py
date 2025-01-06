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


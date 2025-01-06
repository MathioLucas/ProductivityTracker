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

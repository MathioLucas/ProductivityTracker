# ProductivityTracker
# Productivity and Wellness Tracker

##need to add error handling

## Overview
This Python application combines task management, pomodoro timing, and mood tracking into a single productivity tool. It helps users manage their work while monitoring their emotional well-being and focus levels.

ProductivityTracker
Productivity and Wellness Tracker Pro
Overview
This Python application is a comprehensive productivity and wellness management system that combines task management, pomodoro timing, mood tracking, and advanced analytics. It helps users manage their work while monitoring their emotional well-being, energy levels, and focus through an intuitive GUI interface.
Features
Enhanced Task Management

Create and track tasks with categories (Work, Study, Personal, Health)
Priority levels (High, Medium, Low)
Task tagging system
Detailed task descriptions
Track completion status
Task filtering and sorting capabilities

Advanced Pomodoro System

Customizable pomodoro duration (default: 25 minutes)
Adjustable break periods (default: 5 minutes)
Desktop notifications
Track completed pomodoros per task
Visual timer display
Pause/Resume functionality

Comprehensive Wellness Tracking

Rate mood on a 1-10 scale
Track energy levels
Monitor stress levels
Add notes to mood entries
Track wellness patterns over time

Daily Goals System

Set daily task completion targets
Track pomodoro session goals
Goal progress notifications
Daily achievement tracking

Enhanced Statistics and Analytics

Daily productivity overview
Weekly trend analysis
Category-based performance metrics
Mood and energy correlation charts
Task completion patterns
Visual productivity analytics

Data Management

SQLite database storage
Multiple data tables for comprehensive tracking
Automated data organization
Data persistence across sessions

User Interface

Modern tabbed interface
Tree view for task management
Interactive charts and graphs
Status bar for system feedback
Settings management panel

Requirements

Python 3.x
tkinter
ttk (themed widgets)
matplotlib
plyer
sqlite3
datetime
json

Installation
bashCopypip install matplotlib plyer
Database Schema
Tasks Table

id (PRIMARY KEY)
title
description
created_at
completed_at
mood_score
focus_score
pomodoros_completed
category
priority
tags

Mood Tracking Table

id (PRIMARY KEY)
timestamp
mood_score
energy_level
stress_level
notes

Daily Goals Table

id (PRIMARY KEY)
date
goal_type
target_value
achieved_value

Error Handling
The application includes comprehensive error handling for:

Database operations
File operations
User input validation
Timer management
Settings persistence
GUI interactions

Future Enhancements

Data export functionality
Team collaboration features
Integration with calendar systems
Mobile companion app
Cloud synchronization
Advanced reporting featu

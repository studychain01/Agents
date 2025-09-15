"""
Data Manager

This module handles loading, parsing, and managing student data from JSON files.
Provides clean interfaces for accessing profile, calendar, and task information.
"""
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, List


class DataManager:
    """
    Manages student data from JSON files including profiles, calendars, and tasks.
    
    Provides methods for:
    - Loading data from JSON strings
    - Retrieving student profiles by ID
    - Getting upcoming calendar events
    - Filtering active tasks
    - Smart datetime parsing with timezone handling
    """

    def __init__(self):
        """
        Initialize data storage containers.
        All data sources start as None until explicitly loaded through load_data().
        """
        self.profile_data = None
        self.calendar_data = None
        self.task_data = None

    def load_data(self, profile_json: str, calendar_json: str, task_json: str):
        """
        Load and parse multiple JSON data sources simultaneously.

        Args:
            profile_json (str): JSON string containing user profile information
            calendar_json (str): JSON string containing calendar events
            task_json (str): JSON string containing task/todo items

        Note: This method expects valid JSON strings. Any parsing errors will propagate up.
        """
        self.profile_data = json.loads(profile_json)
        self.calendar_data = json.loads(calendar_json)
        self.task_data = json.loads(task_json)

    def get_student_profile(self, student_id: str) -> Dict:
        """
        Retrieve a specific student's profile using their unique identifier.

        Args:
            student_id (str): Unique identifier for the student

        Returns:
            Dict: Student profile data if found, None otherwise

        Implementation Note:
            Uses generator expression with next() for efficient search through profiles,
            avoiding full list iteration when possible.
        """
        if self.profile_data:
            return next((p for p in self.profile_data["profiles"]
                        if p["id"] == student_id), None)
        return None

    def parse_datetime(self, dt_str: str) -> datetime:
        """
        Smart datetime parser that handles multiple formats and ensures UTC timezone.

        Args:
            dt_str (str): DateTime string in ISO format, with or without timezone

        Returns:
            datetime: Parsed datetime object in UTC timezone

        Implementation Note:
            Handles both timezone-aware and naive datetime strings by:
            1. First attempting to parse with timezone information
            2. Falling back to assuming UTC if no timezone is specified
        """
        try:
            # First attempt: Parse ISO format with timezone
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return dt.astimezone(timezone.utc)
        except ValueError:
            # Fallback: Assume UTC if no timezone provided
            dt = datetime.fromisoformat(dt_str)
            return dt.replace(tzinfo=timezone.utc)

    def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """
        Intelligently filter and retrieve upcoming calendar events within a specified timeframe.

        Args:
            days (int): Number of days to look ahead (default: 7)

        Returns:
            List[Dict]: List of upcoming events, chronologically ordered

        Implementation Note:
            - Uses UTC timestamps for consistent timezone handling
            - Implements error handling for malformed event data
            - Only includes events that start in the future up to the specified timeframe
        """
        if not self.calendar_data:
            return []

        now = datetime.now(timezone.utc)
        future = now + timedelta(days=days)

        events = []
        for event in self.calendar_data.get("events", []):
            try:
                # Handle your calendar format: "date" + "time" fields
                if "date" in event and "time" in event:
                    # Use the start time from the time range
                    time_part = event["time"].split("-")[0]  # Get "09:00" from "09:00-10:30"
                    datetime_str = f"{event['date']}T{time_part}:00"
                    start_time = self.parse_datetime(datetime_str)
                # Handle standard format
                elif "start" in event and "dateTime" in event["start"]:
                    start_time = self.parse_datetime(event["start"]["dateTime"])
                else:
                    continue

                if now <= start_time <= future:
                    events.append(event)
            except (KeyError, ValueError) as e:
                print(f"Warning: Could not process event due to {str(e)}")
                continue

        return events

    def get_active_tasks(self) -> List[Dict]:
        """
        Retrieve and filter active tasks, enriching them with parsed datetime information.

        Returns:
            List[Dict]: List of active tasks with parsed due dates

        Implementation Note:
            - Filters for tasks that are:
              1. Not completed ("needsAction" status)
              2. Due in the future
            - Enriches task objects with parsed datetime for easier processing
            - Implements robust error handling for malformed task data
        """
        if not self.task_data:
            return []

        now = datetime.now(timezone.utc)
        active_tasks = []

        # Handle your task format (assignments) and standard format (tasks)
        tasks = self.task_data.get("assignments", [])
        if not tasks:
            tasks = self.task_data.get("tasks", [])
            
        for task in tasks:
            try:
                # Handle your format: "due_date" + "due_time"
                if "due_date" in task and "due_time" in task:
                    datetime_str = f"{task['due_date']}T{task['due_time']}:00"
                    due_date = self.parse_datetime(datetime_str)
                # Handle standard format: "due"
                elif "due" in task:
                    due_date = self.parse_datetime(task["due"])
                else:
                    continue
                    
                # Check if task is active (your format uses "in_progress" vs standard "needsAction")
                if (task.get("status") in ["in_progress", "not_started", "needsAction"] and 
                    due_date > now):
                    # Enrich task object with parsed datetime
                    task["due_datetime"] = due_date
                    active_tasks.append(task)
            except (KeyError, ValueError) as e:
                print(f"Warning: Could not process task due to {str(e)}")
                continue

        return active_tasks

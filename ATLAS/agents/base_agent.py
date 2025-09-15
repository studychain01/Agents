"""
Base Agent Classes

This module contains the base ReActAgent class that provides common functionality
for all specialized agents in the ATLAS system.
"""
from typing import List, Dict
from datetime import datetime, timezone
from models.state import AcademicState


class ReActAgent:
    """
    Base class for ReACT-based agents implementing reasoning and action capabilities.

    Features:
    - Tool management for specific actions
    - Few-shot learning examples
    - Structured thought process
    - Action execution framework
    """

    def __init__(self, llm):
        """
        Initialize the ReActAgent with language model and available tools

        Args:
            llm: Language model instance for agent operations
        """
        self.llm = llm
        # Storage for few-shot examples to guide the agent
        self.few_shot_examples = []

        # Dictionary of available tools with their corresponding methods
        self.tools = {
            "search_calendar": self.search_calendar,      # Calendar search functionality
            "analyze_tasks": self.analyze_tasks,          # Task analysis functionality
            "check_learning_style": self.check_learning_style,  # Learning style assessment
            "check_performance": self.check_performance   # Academic performance checking
        }

    async def search_calendar(self, state: AcademicState) -> List[Dict]:
        """
        Search for upcoming calendar events

        Args:
            state (AcademicState): Current academic state

        Returns:
            List[Dict]: List of upcoming calendar events
        """
        # Get events from calendar or empty list if none exist
        events = state["calendar"].get("events", [])
        # Get current time in UTC
        now = datetime.now(timezone.utc)
        # Filter and return only future events - handle different date formats
        future_events = []
        for event in events:
            try:
                # Handle your calendar format: "date" + "time" fields
                if "date" in event and "time" in event:
                    time_part = event["time"].split("-")[0]  # Get start time
                    event_datetime = datetime.fromisoformat(f"{event['date']}T{time_part}:00")
                    event_datetime = event_datetime.replace(tzinfo=timezone.utc)
                    if event_datetime > now:
                        future_events.append(event)
                # Handle standard format
                elif "start" in event and "dateTime" in event["start"]:
                    event_datetime = datetime.fromisoformat(event["start"]["dateTime"])
                    if event_datetime > now:
                        future_events.append(event)
            except (ValueError, KeyError):
                continue
        return future_events

    async def analyze_tasks(self, state: AcademicState) -> List[Dict]:
        """
        Analyze academic tasks from the current state

        Args:
            state (AcademicState): Current academic state

        Returns:
            List[Dict]: List of academic tasks
        """
        # Return tasks or empty list if none exist - handle your format
        tasks = state["tasks"].get("assignments", [])  # Your format uses "assignments"
        if not tasks:
            tasks = state["tasks"].get("tasks", [])  # Fallback to standard format
        return tasks

    async def check_learning_style(self, state: AcademicState) -> AcademicState:
        """
        Retrieve student's learning style and study patterns

        Args:
            state (AcademicState): Current academic state

        Returns:
            AcademicState: Updated state with learning style analysis
        """
        # Get user profile from state
        profile = state["profile"]

        # Get learning preferences
        learning_data = {
            "style": profile.get("learning_preferences", {}).get("learning_style", {}),
            "patterns": profile.get("learning_preferences", {}).get("study_patterns", {})
        }

        # Add to results in state
        if "results" not in state:
            state["results"] = {}
        state["results"]["learning_analysis"] = learning_data

        return state

    async def check_performance(self, state: AcademicState) -> AcademicState:
        """
        Check current academic performance across courses

        Args:
            state (AcademicState): Current academic state

        Returns:
            AcademicState: Updated state with performance analysis
        """
        # Get user profile from state
        profile = state["profile"]

        # Get course information
        courses = profile.get("academic_info", {}).get("current_courses", [])

        # Add to results in state
        if "results" not in state:
            state["results"] = {}
        state["results"]["performance_analysis"] = {"courses": courses}

        return state

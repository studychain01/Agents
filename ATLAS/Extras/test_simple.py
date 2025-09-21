#!/usr/bin/env python3
"""
Simple test to debug the issue
"""
import sys
import os
import asyncio
import json

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.llm_config import configure_api_keys, get_llm_instance
from models.state import AcademicState
from agents.planner_agent import PlannerAgent
from utils.data_manager import DataManager
from langchain_core.messages import HumanMessage

async def test_simple():
    # Initialize
    configure_api_keys()
    llm = get_llm_instance()
    planner = PlannerAgent(llm)
    
    # Load data
    with open('profile.json', 'r') as f:
        profile_data = json.load(f)
    with open('calendar.json', 'r') as f:
        calendar_data = json.load(f)
    with open('task.json', 'r') as f:
        task_data = json.load(f)
    
    print("Profile data keys:", profile_data.keys())
    print("Calendar data keys:", calendar_data.keys())
    print("Task data keys:", task_data.keys())
    
    print("\nFirst calendar event:", calendar_data["events"][0] if calendar_data.get("events") else "No events")
    print("First assignment:", task_data["assignments"][0] if task_data.get("assignments") else "No assignments")

if __name__ == "__main__":
    asyncio.run(test_simple())

#!/usr/bin/env python3
"""
ATLAS: Academic Task Learning Agent System
Main Application Entry Point

A clean, modular academic assistance system that helps students with:
- Study planning and scheduling
- Task prioritization and management
- Personalized learning recommendations
- Academic workflow optimization

Usage:
    python main.py
"""
import asyncio
import os
import sys
import glob
import json
from rich.console import Console
from rich.panel import Panel

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modular components
from config.llm_config import configure_api_keys, get_llm_instance
from models.state import AcademicState
from agents.planner_agent import PlannerAgent
from agents.notewriter_agent import NoteWriterAgent
from utils.data_manager import DataManager
from langchain_core.messages import HumanMessage


class ATLAS:
    """
    Main ATLAS application class.
    
    Coordinates between different agents and manages the overall workflow
    for academic assistance.
    """
    
    def __init__(self):
        """Initialize the ATLAS system."""
        self.console = Console()
        self.llm = None
        self.data_manager = DataManager()
        
        # Agents will be initialized after LLM setup
        self.planner_agent = None
        self.notewriter_agent = None
        # self.advisor_agent = None  # TODO: Add when extracted
        
    async def initialize(self):
        """Initialize the LLM and agents."""
        try:
            # Configure API keys
            if not configure_api_keys():
                raise ValueError("API key configuration failed")
            
            # Initialize LLM
            self.llm = get_llm_instance()
            self.console.print(f"✅ LLM initialized: {self.llm}")
            
            # Initialize agents
            self.planner_agent = PlannerAgent(self.llm)
            self.notewriter_agent = NoteWriterAgent(self.llm)
            # self.advisor_agent = AdvisorAgent(self.llm)  # TODO: Add when extracted
            
            self.console.print("✅ All agents initialized successfully")
            return True
            
        except Exception as e:
            self.console.print(f"❌ Initialization failed: {e}")
            return False
    
    def load_student_data(self):
        """Load student data from JSON files."""
        try:
            # Look for required JSON files
            required_files = ['profile.json', 'calendar.json', 'task.json']
            missing_files = []
            
            for file in required_files:
                if not os.path.exists(file):
                    missing_files.append(file)
            
            if missing_files:
                self.console.print(f"[yellow]Missing required files: {missing_files}[/yellow]")
                self.console.print("Please ensure you have profile.json, calendar.json, and task.json files.")
                return False
            
            # Load JSON files
            with open('profile.json', 'r') as f:
                profile_data = f.read()
            with open('calendar.json', 'r') as f:
                calendar_data = f.read()
            with open('task.json', 'r') as f:
                task_data = f.read()
            
            # Load data into DataManager
            self.data_manager.load_data(profile_data, calendar_data, task_data)
            
            self.console.print("✅ Student data loaded successfully")
            return True
            
        except Exception as e:
            self.console.print(f"❌ Error loading student data: {e}")
            return False
    
    async def process_query(self, user_query: str) -> str:
        """
        Process a user query using the appropriate agent.
        
        Args:
            user_query: The student's question or request
            
        Returns:
            The agent's response
        """
        try:
            # Get student profile (assuming student_123 as in the original)
            profile = self.data_manager.get_student_profile("student_123")
            if not profile:
                return "Error: Could not load student profile. Please check your profile.json file."
            
            # Create initial state with real data
            state = AcademicState(
                messages=[HumanMessage(content=user_query)],
                profile={"profiles": [profile]},  # Structure expected by agents
                calendar=self.data_manager.calendar_data or {},
                tasks=self.data_manager.task_data or {},
                results={
                    "profile_analysis": {"analysis": f"Student profile loaded for {profile.get('name', 'Unknown')}"}
                }
            )
            
            # For now, default to planner agent
            # TODO: Add coordinator logic to route to appropriate agent
            result = await self.planner_agent(state)
            
            return result.get("notes", "No response generated")
            
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    async def run_interactive_session(self):
        """Run an interactive session with the user."""
        self.console.print("\n[bold magenta]🎓 ATLAS: Academic Task Learning Agent System[/bold magenta]")
        self.console.print("[italic blue]Your AI-powered academic assistant[/italic blue]\n")
        
        while True:
            try:
                # Get user input
                user_query = input("\nWhat can I help you with today? (type 'quit' to exit): ")
                
                if user_query.lower() in ['quit', 'exit', 'q']:
                    self.console.print("\n[bold green]Thanks for using ATLAS! Good luck with your studies! 🎯[/bold green]")
                    break
                
                if not user_query.strip():
                    continue
                
                # Process the query
                self.console.print(f"\n[bold cyan]Processing:[/bold cyan] {user_query}")
                response = await self.process_query(user_query)
                
                # Display response
                self.console.print(Panel(
                    response, 
                    title="📚 Academic Assistant Response", 
                    border_style="green"
                ))
                
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Session interrupted. Goodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"\n[red]Error: {e}[/red]")


async def main():
    """Main application entry point."""
    atlas = ATLAS()
    
    # Initialize the system
    if not await atlas.initialize():
        return 1
    
    # Load student data
    if not atlas.load_student_data():
        return 1
    
    # Run interactive session
    await atlas.run_interactive_session()
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)

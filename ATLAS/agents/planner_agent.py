"""
Planner Agent

This module contains the PlannerAgent class that specializes in creating
comprehensive study plans and academic schedules for students.
"""
import json
from typing import Dict
from datetime import datetime, timezone, timedelta
from langgraph.graph import StateGraph

from agents.base_agent import ReActAgent
from models.state import AcademicState


class PlannerAgent(ReActAgent):
    """
    Specialized agent for creating comprehensive academic plans.
    
    The PlannerAgent analyzes student profiles, calendars, and tasks to create
    personalized study plans that optimize for learning style, energy patterns,
    and deadline management.
    """
    
    def __init__(self, llm):
        super().__init__(llm)  # Initialize parent ReActAgent class
        self.llm = llm
        # Load example scenarios to help guide the AI's responses
        self.few_shot_examples = self._initialize_fewshots()
        # Create the workflow structure
        self.workflow = self.create_subgraph()

    def _initialize_fewshots(self):
        """
        Define example scenarios to help the AI understand how to handle different situations.
        
        Each example shows:
        - Input: The student's request
        - Thought: The analysis process
        - Action: What needs to be done
        - Observation: What was found
        - Plan: The detailed solution
        """
        return [
            {
                "input": "Help with exam prep while managing ADHD and football",
                "thought": "Need to check calendar conflicts and energy patterns",
                "action": "search_calendar",
                "observation": "Football match at 6PM, exam tomorrow 9AM",
                "plan": """ADHD-OPTIMIZED SCHEDULE:
                    PRE-FOOTBALL (2PM-5PM):
                    - 3x20min study sprints
                    - Movement breaks
                    - Quick rewards after each sprint

                    FOOTBALL MATCH (6PM-8PM):
                    - Use as dopamine reset
                    - Formula review during breaks

                    POST-MATCH (9PM-12AM):
                    - Environment: Café noise
                    - 15/5 study/break cycles
                    - Location changes hourly

                    EMERGENCY PROTOCOLS:
                    - Focus lost → jumping jacks
                    - Overwhelmed → room change
                    - Brain fog → cold shower"""
            },
            {
                "input": "Struggling with multiple deadlines",
                "thought": "Check task priorities and performance issues",
                "action": "analyze_tasks",
                "observation": "3 assignments due, lowest grade in Calculus",
                "plan": """PRIORITY SCHEDULE:
                    HIGH-FOCUS SLOTS:
                    - Morning: Calculus practice
                    - Post-workout: Assignments
                    - Night: Quick reviews

                    ADHD MANAGEMENT:
                    - Task timer challenges
                    - Reward system per completion
                    - Study buddy accountability"""
            }
        ]

    def create_subgraph(self) -> StateGraph:
        """
        Create a workflow graph that defines how the planner processes requests:
        1. First analyzes calendar (calendar_analyzer)
        2. Then analyzes tasks (task_analyzer)
        3. Finally generates a plan (plan_generator)
        """
        # Initialize a new graph using our AcademicState structure
        subgraph = StateGraph(AcademicState)

        # Add each processing step as a node in our graph
        subgraph.add_node("calendar_analyzer", self.calendar_analyzer)
        subgraph.add_node("task_analyzer", self.task_analyzer)
        subgraph.add_node("plan_generator", self.plan_generator)

        # Connect the nodes in the order they should execute
        subgraph.add_edge("calendar_analyzer", "task_analyzer")
        subgraph.add_edge("task_analyzer", "plan_generator")

        # Set where the workflow begins
        subgraph.set_entry_point("calendar_analyzer")

        # Prepare the graph for use
        return subgraph.compile()

    async def calendar_analyzer(self, state: AcademicState) -> AcademicState:
        """
        Analyze the student's calendar to find:
        - Available study times
        - Potential scheduling conflicts
        - Energy patterns throughout the day
        """
        # Get calendar events for the next 7 days
        events = state["calendar"].get("events", [])
        now = datetime.now(timezone.utc)
        future = now + timedelta(days=7)

        # Filter to only include upcoming events - handle different date formats
        filtered_events = []
        for event in events:
            try:
                # Handle your calendar format: "date" + "time" fields
                if "date" in event and "time" in event:
                    # Combine date and time, use start of time range
                    time_part = event["time"].split("-")[0]  # Get start time from "09:00-10:30"
                    event_datetime = datetime.fromisoformat(f"{event['date']}T{time_part}:00")
                    event_datetime = event_datetime.replace(tzinfo=timezone.utc)
                    
                    if now <= event_datetime <= future:
                        filtered_events.append(event)
                # Handle standard format: "start" with "dateTime"        
                elif "start" in event and "dateTime" in event["start"]:
                    event_datetime = datetime.fromisoformat(event["start"]["dateTime"])
                    if now <= event_datetime <= future:
                        filtered_events.append(event)
            except (ValueError, KeyError) as e:
                print(f"Warning: Could not process event {event.get('title', 'Unknown')}: {e}")
                continue

        # Create prompt for the AI to analyze the calendar
        prompt = """Analyze calendar events and identify:
        Events: {events}

        Focus on:
        - Available time blocks
        - Energy impact of activities
        - Potential conflicts
        - Recovery periods
        - Study opportunity windows
        - Activity patterns
        - Schedule optimization
        """

        # Ask AI to analyze the calendar
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(filtered_events)}
        ]

        response = await self.llm.agenerate(messages)

        # Return the analysis results
        return {
            "results": {
                "calendar_analysis": {
                    "analysis": response
                }
            }
        }

    async def task_analyzer(self, state: AcademicState) -> AcademicState:
        """
        Analyze tasks to determine:
        - Priority order
        - Time needed for each task
        - Best approach for completion
        """
        # Handle your task format (assignments) and standard format (tasks)
        tasks = state["tasks"].get("assignments", [])
        if not tasks:
            tasks = state["tasks"].get("tasks", [])

        # Create prompt for AI to analyze tasks
        prompt = """Analyze tasks and create priority structure:
        Tasks: {tasks}

        Consider:
        - Urgency levels
        - Task complexity
        - Energy requirements
        - Dependencies
        - Required focus levels
        - Time estimations
        - Learning objectives
        - Success criteria
        """

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(tasks)}
        ]

        response = await self.llm.agenerate(messages)

        return {
            "results": {
                "task_analysis": {
                    "analysis": response
                }
            }
        }

    async def plan_generator(self, state: AcademicState) -> AcademicState:
        """
        Create a comprehensive study plan by combining:
        - Profile analysis (student's learning style)
        - Calendar analysis (available time)
        - Task analysis (what needs to be done)
        """
        # Gather all previous analyses
        profile_analysis = state["results"]["profile_analysis"]
        calendar_analysis = state["results"]["calendar_analysis"]
        task_analysis = state["results"]["task_analysis"]

        # Create detailed prompt for AI to generate plan
        prompt = f"""AI Planning Assistant: Create focused study plan using ReACT framework.

          INPUT CONTEXT:
          - Profile Analysis: {profile_analysis}
          - Calendar Analysis: {calendar_analysis}
          - Task Analysis: {task_analysis}

          EXAMPLES:
          {json.dumps(self.few_shot_examples, indent=2)}

          INSTRUCTIONS:
          1. Follow ReACT pattern:
            Thought: Analyze situation and needs
            Action: Consider all analyses
            Observation: Synthesize findings
            Plan: Create structured plan

          2. Address:
            - ADHD management strategies
            - Energy level optimization
            - Task chunking methods
            - Focus period scheduling
            - Environment switching tactics
            - Recovery period planning
            - Social/sport activity balance

          3. Include:
            - Emergency protocols
            - Backup strategies
            - Quick wins
            - Reward system
            - Progress tracking
            - Adjustment triggers

          Pls act as an intelligent tool to help the students reach their goals or overcome struggles and answer with informal words.

          FORMAT:
          Thought: [reasoning and situation analysis]
          Action: [synthesis approach]
          Observation: [key findings]
          Plan: [actionable steps and structural schedule]
          """

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": state["messages"][-1].content}
        ]
        
        # Generate the plan with moderate creativity
        response = await self.llm.agenerate(messages, temperature=0.5)

        return {
            "results": {
                "final_plan": {
                    "plan": response
                }
            }
        }

    async def __call__(self, state: AcademicState) -> Dict:
        """
        Main execution method that runs the entire planning workflow:
        1. Analyze calendar
        2. Analyze tasks
        3. Generate plan
        """
        try:
            final_state = await self.workflow.ainvoke(state)
            # Get the final plan from plan_generator
            final_plan = final_state["results"].get("final_plan", {})
            plan_content = final_plan.get("plan", "No plan generated")
            return {"notes": plan_content}
        except Exception as e:
            return {"notes": f"Error generating plan: {str(e)}. Please try again."}

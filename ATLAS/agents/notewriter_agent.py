"""
NoteWriter Agent

This module contains the NoteWriterAgent class that specializes in creating
personalized study materials and notes based on student learning styles.
"""
import json
from typing import Dict
from langgraph.graph import StateGraph, START, END

from agents.base_agent import ReActAgent
from models.state import AcademicState


class NoteWriterAgent(ReActAgent):
    """
    NoteWriter agent with its own subgraph workflow for note generation.
    This agent specializes in creating personalized study materials by analyzing
    learning styles and generating structured notes.
    """

    def __init__(self, llm):
        """Initialize the NoteWriter agent with an LLM backend and example templates.

        Args:
            llm: Language model instance for text generation
        """
        super().__init__(llm)
        self.llm = llm
        self.few_shot_examples = [
            {
                "input": "Need to cram Calculus III for tomorrow",
                "template": "Quick Review",
                "notes": """CALCULUS III ESSENTIALS:

                1. CORE CONCEPTS (80/20 Rule):
                   • Multiple Integrals → volume/area
                   • Vector Calculus → flow/force/rotation
                   • KEY FORMULAS:
                     - Triple integrals in cylindrical/spherical coords
                     - Curl, divergence, gradient relationships

                2. COMMON EXAM PATTERNS:
                   • Find critical points
                   • Calculate flux/work
                   • Optimize with constraints

                3. QUICKSTART GUIDE:
                   • Always draw 3D diagrams
                   • Check units match
                   • Use symmetry to simplify

                4. EMERGENCY TIPS:
                   • If stuck, try converting coordinates
                   • Check boundary conditions
                   • Look for special patterns"""
            }
        ]
        self.workflow = self.create_subgraph()

    def create_subgraph(self) -> StateGraph:
        """Creates NoteWriter's internal workflow as a state machine.

        The workflow consists of two main steps:
        1. Analyze learning style and content requirements
        2. Generate personalized notes

        Returns:
            StateGraph: Compiled workflow graph
        """
        subgraph = StateGraph(AcademicState)

        # Define the core workflow nodes
        subgraph.add_node("notewriter_analyze", self.analyze_learning_style)
        subgraph.add_node("notewriter_generate", self.generate_notes)

        # Create the workflow sequence:
        # START -> analyze -> generate -> END
        subgraph.add_edge(START, "notewriter_analyze")
        subgraph.add_edge("notewriter_analyze", "notewriter_generate")
        subgraph.add_edge("notewriter_generate", END)

        return subgraph.compile()

    async def analyze_learning_style(self, state: AcademicState) -> AcademicState:
        """Analyzes student profile and request to determine optimal note structure."""
        profile = state["profile"]
        learning_style = profile["learning_preferences"]["learning_style"]

        prompt = f"""Analyze content requirements and determine optimal note structure:

        STUDENT PROFILE:
        - Learning Style: {json.dumps(learning_style, indent=2)}
        - Request: {state['messages'][-1].content}

        FORMAT:
        1. Key Topics (80/20 principle)
        2. Learning Style Adaptations
        3. Time Management Strategy
        4. Quick Reference Format

        FOCUS ON:
        - Essential concepts that give maximum understanding
        - Visual and interactive elements
        - Time-optimized study methods
        """

        response = await self.llm.agenerate([
            {"role": "system", "content": prompt}
        ])

        return {
            "results": {
                "learning_analysis": {
                    "analysis": response
                }
            }
        }

    async def generate_notes(self, state: AcademicState) -> AcademicState:
        """Generates personalized study notes based on the learning analysis."""
        analysis = state["results"].get("learning_analysis", "")
        learning_style = state["profile"]["learning_preferences"]["learning_style"]

        # Build prompt using analysis and few-shot examples
        prompt = f"""Create concise, high-impact study materials based on analysis:

        ANALYSIS: {analysis}
        LEARNING STYLE: {json.dumps(learning_style, indent=2)}
        REQUEST: {state['messages'][-1].content}

        EXAMPLES:
        {json.dumps(self.few_shot_examples, indent=2)}

        FORMAT:
        **THREE-WEEK INTENSIVE STUDY PLANNER**

        [Generate structured notes with:]
        1. Weekly breakdown
        2. Daily focus areas
        3. Core concepts
        4. Emergency tips
        """

        response = await self.llm.agenerate([
            {"role": "system", "content": prompt}
        ])
        
        return {
            "results": {
                "generated_notes": {
                    "notes": response
                }
            }
        }

    async def __call__(self, state: AcademicState) -> Dict:
        """Main execution method for the NoteWriter agent."""
        try:
            final_state = await self.workflow.ainvoke(state)
            notes = final_state["results"].get("generated_notes", {})
            return {"notes": final_state["results"].get("generated_notes")}
        except Exception as e:
            return {"notes": f"Error generating notes: {str(e)}. Please try again."}

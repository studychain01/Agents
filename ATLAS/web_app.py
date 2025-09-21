#!/usr/bin/env python3
"""
ATLAS Web Application
A modern web frontend for the Academic Task Learning Agent System
"""
import sys
import os
import asyncio
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import ATLAS components
from config.llm_config import configure_api_keys, get_llm_instance
from models.state import AcademicState
from agents.planner_agent import PlannerAgent
from agents.notewriter_agent import NoteWriterAgent
from utils.data_manager import DataManager
from langchain_core.messages import HumanMessage

app = Flask(__name__, 
           template_folder='web/templates',
           static_folder='web/static')
CORS(app)

# Global ATLAS instance
atlas_instance = None

class WebATLAS:
    """Web version of ATLAS system"""
    
    def __init__(self):
        self.llm = None
        self.data_manager = DataManager()
        self.planner_agent = None
        self.notewriter_agent = None
        self.initialized = False
    
    async def initialize(self):
        """Initialize the ATLAS system"""
        try:
            if not configure_api_keys():
                raise ValueError("API key configuration failed")
            
            self.llm = get_llm_instance()
            self.planner_agent = PlannerAgent(self.llm)
            self.notewriter_agent = NoteWriterAgent(self.llm)
            
            # Load student data
            if self.load_student_data():
                self.initialized = True
                return True
            return False
            
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False
    
    def load_student_data(self):
        """Load student data from JSON files"""
        try:
            required_files = ['profile.json', 'calendar.json', 'task.json']
            for file in required_files:
                if not os.path.exists(file):
                    print(f"Missing file: {file}")
                    return False
            
            with open('profile.json', 'r') as f:
                profile_data = f.read()
            with open('calendar.json', 'r') as f:
                calendar_data = f.read()
            with open('task.json', 'r') as f:
                task_data = f.read()
            
            self.data_manager.load_data(profile_data, calendar_data, task_data)
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    async def process_query(self, user_query: str, agent_type: str = "planner"):
        """Process user query with specified agent"""
        try:
            if not self.initialized:
                return "System not initialized. Please refresh the page."
            
            profile = self.data_manager.get_student_profile("student_123")
            if not profile:
                return "Error: Could not load student profile."
            
            state = AcademicState(
                messages=[HumanMessage(content=user_query)],
                profile={"profiles": [profile]},
                calendar=self.data_manager.calendar_data or {},
                tasks=self.data_manager.task_data or {},
                results={
                    "profile_analysis": {"analysis": f"Student profile loaded for {profile.get('name', 'Unknown')}"}
                }
            )
            
            # Route to appropriate agent
            if agent_type == "notewriter":
                result = await self.notewriter_agent(state)
            else:  # default to planner
                result = await self.planner_agent(state)
            
            return result.get("notes", "No response generated")
            
        except Exception as e:
            return f"Error processing query: {str(e)}"

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def api_query():
    """API endpoint for processing queries"""
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        agent_type = data.get('agent', 'planner')
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(
                atlas_instance.process_query(user_query, agent_type)
            )
        finally:
            loop.close()
        
        return jsonify({
            'response': response,
            'agent': agent_type,
            'query': user_query
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def api_status():
    """Check system status"""
    return jsonify({
        'initialized': atlas_instance.initialized if atlas_instance else False,
        'agents': ['planner', 'notewriter'],
        'status': 'ready' if (atlas_instance and atlas_instance.initialized) else 'initializing'
    })

def initialize_atlas():
    """Initialize ATLAS system"""
    global atlas_instance
    atlas_instance = WebATLAS()
    
    # Initialize in background
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(atlas_instance.initialize())
    finally:
        loop.close()

# Initialize ATLAS when module loads
initialize_atlas()

if __name__ == '__main__':
    print("🎓 Starting ATLAS Web Application...")
    print("🌐 Access the web interface at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

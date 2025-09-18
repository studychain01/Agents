from typing import TypedDict 
from langgraph.graph import StateGraph, END 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate 
import os 
from dotenv import load_dotenv 
import re

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn 

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class State(TypedDict):
    """Represents the state of the essay graind process."""
    essay: str
    relevance_score: float 
    grammar_score: float 
    structure_score: float 
    depth_score: float 
    final_score: float 

llm = ChatOpenAI(model="gpt-4o-mini")

def extract_score(content: str) -> float:
    """Extract the numeric score from the LLM's response."""
    match = re.search(r'Score:\s*(\d+(\.\d+)?)', content)
    if match: 
        return float(match.group(1))
    raise ValueError(f"Could not extract score from: {content}")

def check_relevance(state: State) -> State:
    """Check the relevance of the essay."""

    prompt = ChatPromptTemplate.from_template(
        "Analyze the relevance of the following essay to the given topic."
        "Provide a relevance score between 0 and 1."
        "Your response should start with 'Score: ' followed by the numeric score,"
        "then provide your explanation.\n\nEssay: {essay}"
    )

    result = llm.invoke(prompt.format(essay=state["essay"]))
    try: 
        state["relevance_score"] = extract_score(result.content)

    except ValueError as e: 
        print(f"Error in check_relevance: {e}")
        state["relevance_score"] = 0.0
    return state 

def check_grammar(state: State) -> State:
    """Check the grammar of the essay."""
    prompt = ChatPromptTemplate.from_template(
        "Analyze the grammar and language usage in the following essay."
        "Provide a grammar score between 0 and 1."
        "Your response should start with 'Score: ' followed by the numeric score, "
        "then provide your explanation. \n\nEssay: {essay}"
    )

    result = llm.invoke(prompt.format(essay=state["essay"]))

    try: 
        state["grammar_score"] = extract_score(result.content)
    except ValueError as e:
        print(f"Error in check_grammar: {e}")
        state["grammar_score"] = 0.0
    return state 


def analyze_structure(state: State) -> State:
    """Analyze the structure of the essay. """
    prompt = ChatPromptTemplate.from_template(
        "Analyze the structure of the following essay"
        "Provide a structure score between 0 and 1"
        "Your response should start with 'Score: ' followed by the numeric score"
        "then provide your explanation. \n\nEssay: {essay}"
    )
    result = llm.invoke(prompt.format(essay=state["essay"]))

    try: 
        state["structure_score"]  = extract_score(result.content)
    except ValueError as e:
        print(f"Error in analyze_structure: {e}")
        state["structure_score"] = 0.0
    return state 

def evaluate_depth(state: State) -> State:
    """Evaluate the depth of the essay."""
    prompt = ChatPromptTemplate.from_template(
        "Evaluate the depth of the following essay"
        "Provide a depth score between 0 and 1"
        "Your response should start with 'Score: ' followed by the numeric score"
        "then provide your explanation. \n\nEssay: {essay}"
    )

    result = llm.invoke(prompt.format(essay=state["essay"]))
    try: 
        state["depth_score"] = extract_score(result.content)

    except ValueError as e: 
        print(f"Error in evaluate_depth: {e}")
        state["depth_score"] = 0.0
    return state 

def calculate_final_score(state: State) -> State:
    """Calculate the final score based on individual component scores."""
    state["final_score"] = (
        state["relevance_score"] * 0.3 + 
        state["grammar_score"] * 0.2 +
        state["structure_score"] * 0.2 + 
        state["depth_score"] * 0.3
    )
    return state 

workflow = StateGraph(State)

workflow.add_node("check_relevance", check_relevance)
workflow.add_node("check_grammar", check_grammar)
workflow.add_node("analyze_structure", analyze_structure)
workflow.add_node("evaluate_depth", evaluate_depth)
workflow.add_node("calculate_final_score", calculate_final_score)

workflow.add_conditional_edges(
    "check_relevance",
    lambda x: "check_grammar" if x["relevance_score"] <0.5 else "calculate_final_score"
)
workflow.add_conditional_edges(
    "check_grammar",
    lambda x: "analyze_structure" if x["grammar_score"] > 0.6 else "calculate_final_score"
)

workflow.add_conditional_edges(
    "analyze_structure",
    lambda x: "evaluate_depth" if x["structure_score"] > 0.7 else "calculate_final_score"
)

workflow.add_conditional_edges(
    "evaluate_depth",
    lambda x: "calculate_final_score"
)

workflow.set_entry_point("check_relevance")
workflow.add_edge("calculate_final_score", END)

app = workflow.compile()

def grade_essay(essay: str) -> dict:
    """Grade the given essay using the defined workflow."""
    initial_state = State(
        essay=essay, 
        relevance_score=0.0,
        grammar_score=0.0,
        structure_score=0.0,
        depth_score=0.0,
        final_score=0.0
    )

    result = app.invoke(initial_state)
    return result 

# Pydantic models for API
class EssayRequest(BaseModel):
    essay: str

class EssayResponse(BaseModel):
    essay: str
    relevance_score: float
    grammar_score: float
    structure_score: float
    depth_score: float
    final_score: float
    grade: str

# FastAPI app
fastapi_app = FastAPI(title="Essay Grading API", description="AI-powered essay grading system")

@fastapi_app.post("/grade-essay", response_model=EssayResponse)
async def grade_essay_endpoint(request: EssayRequest):
    """Grade an essay and return detailed scores."""
    try:
        result = grade_essay(request.essay)
        
        # Convert final score to letter grade
        final_score = result["final_score"]
        if final_score >= 0.9:
            grade = "A"
        elif final_score >= 0.8:
            grade = "B"
        elif final_score >= 0.7:
            grade = "C"
        elif final_score >= 0.6:
            grade = "D"
        else:
            grade = "F"
        
        return EssayResponse(
            essay=result["essay"],
            relevance_score=result["relevance_score"],
            grammar_score=result["grammar_score"],
            structure_score=result["structure_score"],
            depth_score=result["depth_score"],
            final_score=final_score,
            grade=grade
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error grading essay: {str(e)}")

@fastapi_app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Essay grading API is running"}

@fastapi_app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Essay Grading API",
        "endpoints": {
            "/grade-essay": "POST - Grade an essay",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }

if __name__ == "__main__":
    # For testing purposes, you can still run the original functionality
    # with open("essay.txt", "r") as file: 
    #     real_essay = file.read()
    # result = grade_essay(real_essay)
    # print(result)
    
    # Run FastAPI server
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

import os 
from typing import TypedDict, List 
from langgraph.graph import StateGraph, END 
from langchain.prompts import PromptTemplate 
from langchain_openai import ChatOpenAI 
from langchain.schema import HumanMessage 
from langchain_core.runnables.graph import MermaidDrawMethod
from IPython.display import display, Image 

from dotenv import load_dotenv 

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class State(TypedDict): 
    text: str 
    classification: str 
    entities: List[str]
    summary: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def classification_node(state: State):
    ''' Classify text into one of the categories: News, Blog, Research, or Other '''

    prompt = PromptTemplate(
        #defining the input variables
        input_variables=["text"],

        template="Classify the following text into one of the categories: News, Blog, Research, or Other.\n\nText:{text}\n\nCategory:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    classification = llm.invoke([message]).content.strip()
    return {"classification": classification}

def entity_extraction_node(state: State):
    '''Extract all the entities (Person, Organization, Location) from the text'''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Extract all the entities (Person, Organization, Location) from the following text. Provide the result as a comma-seperated list. \n\nText:{text}\n\nEntities:"
    )

    message = HumanMessage(content=prompt.format(text=state["text"]))
    entities = llm.invoke([message]).content.strip().split(".")
    return {"entities": entities}

def summarization_node(state: State):
    ''' Summarize the text in one short sentence '''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize the following text in one short sentence. .\n\nText:{text}\n\nSummary:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    summary = llm.invoke([message]).content.strip()
    return {"summary": summary}


workflow = StateGraph(State)

# Add nodes to the graph
workflow.add_node("classification", classification_node)
workflow.add_node("entity_extraction", entity_extraction_node)
workflow.add_node("summarization", summarization_node)

# Add edges to the graph
workflow.set_entry_point("classification")
workflow.add_edge("classification", "entity_extraction") 
workflow.add_edge("entity_extraction", "summarization")
workflow.add_edge("summarization", END)

app = workflow.compile()


sample_text = """
OpenAI has announced the GPT-4 model, which is a large multimodal model that exhibits human-level performance on various professional benchmarks. It is developed to improve the alignment and safety of AI systems.
additionally, the model is designed to be more efficient and scalable than its predecessor, GPT-3. The GPT-4 model is expected to be released in the coming months and will be available to the public for research and development purposes.
"""

state_input = {"text": sample_text}
result = app.invoke(state_input)

print("Classification:", result["classification"])
print("\nEntities:", result["entities"])
print("\nSummary:", result["summary"])


# Save the graph visualization as a PNG file
try:
    graph_png = app.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
    )
    with open("workflow_graph.png", "wb") as f:
        f.write(graph_png)
    print("\n📊 Graph visualization saved as 'workflow_graph.png'")
    
    # Try to open the image (works on macOS)
    import subprocess
    subprocess.run(["open", "workflow_graph.png"], check=False)
except Exception as e:
    print(f"\n⚠️ Could not generate graph visualization: {e}")
    print("You can still see the text-based graph structure above.")
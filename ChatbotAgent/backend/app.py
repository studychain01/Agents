from langchain_openai import ChatOpenAI 
from langchain_core.runnables.history import RunnableWithMessageHistory 
from langchain_community.chat_message_histories import ChatMessageHistory 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os 
from dotenv import load_dotenv 

# Load environment variables (for local development)
load_dotenv()

# Set OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")
os.environ["OPENAI_API_KEY"] = openai_api_key

llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=1000, temperature=0)

store = {}

def get_chat_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm 

chain_with_history = RunnableWithMessageHistory(
    #chain and history are positional, rest are flexible
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="history"
)

class ChatRequest(BaseModel):
    session_id: str
    input: str

fastapi_app = FastAPI(title="Chatbot API", description="A simple chatbot API")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@fastapi_app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Chatbot API is running"}

@fastapi_app.post("/chat")
async def chatbot(request: ChatRequest):
    response = chain_with_history.invoke(
        {"input": request.input},
        config={"configurable": {"session_id": request.session_id}},
    )
    return {"response": response.content}


import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=1000, temperature=0.5, api_key=API_KEY)

template = """
You are a helpful assistant. Your task is to answer the user's question to the best of your ability. 
User's question: {question}

Please provide a clear and concise answer. 
"""

prompt = PromptTemplate(template=template, input_variables=["question"])

qa_chain = prompt | llm 

def get_answer(question):
    input_variables = {"question": question}
    response = qa_chain.invoke(input_variables).content
    return response 

question = "What is the capital of France?"
answer = get_answer(question)
print(f"Question: {question}")
print(f"Answer: {answer}")

user_question = input("Enter your question: ")
user_answer = get_answer(user_question)
print(f"Answer: {user_answer}")

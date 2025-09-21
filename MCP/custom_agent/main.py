import os 
import json 
from typing import List, Dict, Any 

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client 

from anthropic import Anthropic 

os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic()

mcp_server_path = ""
print("Setup complete")


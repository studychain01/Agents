async def execute_tool(tool_name: str, arguments: Dict[str, Any]):
    """
    Execute a specific tool provided by the MCP server. 

    Args:
        tool_name: The name of the tool to execute. 
        arguments: A dictionary of arguments to pass to the tool. 
    
    Returns: 
        The result from executing the tool
    
    """
    
    # ANSI color codes for better log visibility
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    SEP = "-" * 40

    server_params = StdioServerParameters(
        command="python",
        args=[mcp_server_path],
    )

    print(f"{YELLOW}{SEP}")
    print(f"⚙️ EXECUTION PHASE: Running tool '{tool_name}'")
    print(f"📋 Arguments: {json.dumps(arguments, indent=2)}")
    print(f"{SEP}{RESET}")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Call the specific tool with the provided arguments
            print(f"{BLUE}📡 Sending request to MCP server...{RESET}")
            result = await session.call_tool(tool_name, arguments)
            
            print(f"{GREEN}✅ Tool execution complete{RESET}")
            
            # Format result preview for cleaner output
            result_preview = str(result)
            if len(result_preview) > 150:
                result_preview = result_preview[:147] + "..."
                
            print(f"{BLUE}📊 Result: {result_preview}{RESET}")
            print(f"{SEP}")
            
            return result

print("Tool execution function defined")





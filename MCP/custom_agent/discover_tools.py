async def discover_tools():
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RESET = "\033[0m"
    SEP = "=" * 40

    server_params = StdioServerParameters(
        command="python",
        args=[mcp_server_path]
    )

    print(f"{BLUE}{SEP}\n🔍 DISCOVERY PHASE: Connecting to MCP server...{RESET}")

    # Connect to the server via stdio 
    async with stdio_client(server_params) as (read, write):
        async with  ClientSession(read, write) as session: 
            print(f"{BLUE}📡 Initializing MCP connection...{RESET}")
            await session.initialize()
        
            print(f"{BLUE}🔎 Discovering available tools...{RESET}")
            tools = await session.list_tools()

            tool_info = []
            for tool_type, tool_list in tools:
                if tool_type == "tools":
                    for tool in tool_list:
                        tool_info.append({
                            "name": tool.name, 
                            "description": tool.description,
                            "schema": tool.inputSchema
                        })
            
            print(f"{GREEN}✅ Successfully discovered {len(tool_info)} tools{RESET}")
            print(f"{SEP}")
            return tool_info

print("Tool discovery function defined") 
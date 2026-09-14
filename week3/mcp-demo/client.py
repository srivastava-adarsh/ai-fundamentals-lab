import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

#Tell the client how to launch our server
server_params = StdioServerParameters(
    command="uv",
    args = ["run", "python", "server.py"]
)

async def main():
    #Connect to the server over stdio
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read,write) as session:
            #Handshake
            await session.initialize()

            #Discover available tools
            tools = await session.list_tools()
            print("=== Tools the server offer ===")
            for tool in tools.tools:
                print (f" {tool.name}:  {tool.description}")

            #Call the add tool
            print("\n==== Calling add(2,3) ====")
            result = await session.call_tool("add", {"a": 2, "b":3})
            print("Result:" , result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())


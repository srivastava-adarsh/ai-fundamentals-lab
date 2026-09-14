from mcp.server.fastmcp import FastMCP

#Create an MCP server named "demo"

mcp = FastMCP("demo")

#Expose the tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result"""
    return a + b

if __name__ == "__main__" :
    mcp.run()

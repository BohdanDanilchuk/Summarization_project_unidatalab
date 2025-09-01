from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse
from starlette.requests import Request

from rag import retrieve_answer
from summarization import summarize_dialog_text

PORT = 56000

mcp_server = FastMCP("TOOLServer", host="0.0.0.0", port=PORT)

@mcp_server.tool(description="Use this tool to answer questions about the student or general knowledge.")
def answer(query: str) -> str:
    return retrieve_answer(query)

@mcp_server.tool(description="Use this tool ONLY to create a short, concise summary of a dialogue and not add other detail.")
def summarize(dialog_text: str) -> str:
    return summarize_dialog_text(dialog_text)

@mcp_server.custom_route("/", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({"status": "ok", "message": "Unified MCP server is running"})

if __name__ == "__main__":
    mcp_server.run(transport="streamable-http")
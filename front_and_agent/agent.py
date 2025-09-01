import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import httpx

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def wait_for_mcp(url="http://mcp_server:56000/", timeout=30):
    async with httpx.AsyncClient() as client:
        for _ in range(timeout):
            try:
                r = await client.get(url)
                if r.status_code == 200:
                    return
            except Exception:
                await asyncio.sleep(1)
        raise TimeoutError("MCP server is not responding")

async def build_agent():
    servers = {
        "unified": {"transport": "streamable_http", "url": "http://mcp_server:56000/mcp/"},
    }

    await wait_for_mcp("http://mcp_server:56000/")  

    mcp_client = MultiServerMCPClient(servers)
    tools = await mcp_client.get_tools()

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=OPENAI_API_KEY,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant.\n"
                   "You can use the following tools:\n{tools}\n"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]).partial(tools="\n".join(f"{t.name}: {t.description}" for t in tools))

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return executor

agent = None

async def build_agent_global():
    global agent
    if agent is None:
        agent = await build_agent()
    return agent

async def run_agent_async(query: str) -> str:
    agent = await build_agent_global()
    result = await agent.ainvoke({"input": query})
    final_output = result.get("output", str(result))
    return final_output

def run_agent(query: str) -> str:
    return asyncio.run(run_agent_async(query))

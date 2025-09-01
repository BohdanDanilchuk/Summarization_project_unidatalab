Summarization Project: AI Agent with MCP Tools
This project demonstrates a two-container microservices setup:
Container 1 – Streamlit + LangChain Agent
Runs a web interface (Streamlit) and an AI agent that orchestrates requests. The agent connects to the MCP server and decides which tool to use.
Container 2 – MCP Server
Exposes tools via HTTP:

RAG Tool → retrieves and answers questions from biography.pdf using vector search & summarization.
Summarization Tool → generates concise summaries of dialogues using a fine-tuned transformer model.

Prerequisites
Docker
Install Docker from the official website.
OpenAI API Key
In the project root, create a .env file:
envOPENAI_API_KEY="your_openai_api_key_here"
How to Start
First Launch
Run the following command to build and start both containers:
bashdocker-compose up --build
Wait until dependencies are installed. Stop with Ctrl+C.
Next Runs
Start services without rebuilding:
bashdocker-compose up
Running the Client
Once containers are running, open:
👉 http://localhost:8501
This launches the Streamlit web interface where you can chat with the agent.
How It Works
MCP Server (container 2)

Runs at http://mcp_server:56000/ inside the Docker network.
Provides REST endpoints for tools:

/mcp/ – tool access
/ – health check



LangChain Agent (container 1)

Queries MCP server to discover available tools.
Uses gpt-4o-mini as reasoning engine.
Delegates user queries to either:

answer(query) → RAG biography Q&A
summarize(dialog_text) → Dialogue summarization



Streamlit UI (container 1)

Provides chat-style interface with conversation memory.
Sends user input to the agent and displays results.

Project Structure
Summarization_project/
├── front_and_agent/
│   ├── agent.py              # LangChain agent logic
│   ├── app.py               # Streamlit UI
│   ├── Dockerfile           # Dockerfile for frontend + agent
│   └── requirements.txt
│
├── tool_mcp/
│   ├── mcp_server.py        # MCP server exposing tools
│   ├── rag.py              # RAG (biography retrieval & QnA)
│   ├── summarization.py     # Summarization tool
│   ├── biography.pdf        # Knowledge base for RAG
│   ├── Dockerfile          # Dockerfile for MCP server
│   └── requirements_mcp.txt
│
├── docker-compose.yml
├── .env
└── README.md
Troubleshooting
Check Container Status
bashdocker-compose ps
View Logs
bash# All services
docker-compose logs -f

# Specific service
docker-compose logs -f mcp_server
docker-compose logs -f frontend
Test MCP Server Health
bashcurl http://localhost:56000/
Rebuild Containers
bashdocker-compose down
docker-compose build --no-cache
docker-compose up
Features

Conversational AI Interface with Streamlit
RAG-based Question Answering from PDF documents
Text Summarization using fine-tuned transformer models
Microservices Architecture with Docker containers
Tool Discovery via MCP (Model Context Protocol)
Persistent Chat History during session

Technologies Used

Frontend: Streamlit, LangChain
Backend: FastMCP, Starlette
AI/ML: OpenAI GPT-4o-mini, Transformers, LlamaIndex
Infrastructure: Docker, Docker Compose
Protocols: MCP (Model Context Protocol)


🚀 Ready to chat with your AI agent! Open http://localhost:8501 and start asking questions about the biography or request dialogue summaries.
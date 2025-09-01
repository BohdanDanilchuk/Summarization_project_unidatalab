# Summarization Project: AI Agent with MCP Tools

This project demonstrates a **two-container microservices setup**:

- **Container 1 – Streamlit + LangChain Agent**  
  Runs a web interface (Streamlit) and an AI agent that orchestrates requests.  
  The agent connects to the MCP server and decides which tool to use.  

- **Container 2 – MCP Server**  
  Exposes tools via HTTP:  
  - **RAG Tool** → retrieves and answers questions from `biography.pdf` using vector search & summarization.  
  - **Summarization Tool** → generates concise summaries of dialogues using a fine-tuned transformer model.  

---

## Prerequisites

### Docker
Install Docker from the [official website](https://www.docker.com/).

### OpenAI API Key
In the project root, create a `.env` file:

```bash
OPENAI_API_KEY="your_openai_api_key_here"

## How to Start

### First Launch
Run the following command to build and start both containers:

```bash
docker-compose up --build

Wait until dependencies are installed.
Stop with Ctrl+C.

### Next Runs
Start services without rebuilding:

```bash
docker-compose up

---

## Running the Client
Once containers are running, open:
http://localhost:8501

This launches the Streamlit web interface where you can chat with the agent.
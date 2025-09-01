import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, Settings, SummaryIndex, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from openai import OpenAI as OpenAI_Client  

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

Settings.llm = OpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key)
Settings.embed_model = OpenAIEmbedding(openai_api_key=openai_api_key)
llm_client = OpenAI_Client(api_key=openai_api_key)

document = SimpleDirectoryReader(input_files=["/app/biography.pdf"]).load_data()
splitter = SentenceSplitter(chunk_size=500, chunk_overlap=50)
nodes = splitter.get_nodes_from_documents(document)

summary_index = SummaryIndex(nodes)
vector_index = VectorStoreIndex(nodes)

summary_query_engine = summary_index.as_query_engine(response="tree_summarize", use_async=True)
vector_query_engine = vector_index.as_query_engine()

summary_tool = QueryEngineTool.from_defaults(
    query_engine=summary_query_engine,
    description="Useful for summarization questions related to biography"
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="Useful for retrieving specific context from the biography paper"
)

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[summary_tool, vector_tool],
    verbose=True
)

def fallback_answer(query: str) -> str:
    resp = llm_client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "user", "content": query}]
    )
    return resp.choices[0].message.content

def retrieve_answer(query: str) -> str:
    try:
        response = query_engine.query(query)
    except ValueError:
        response = fallback_answer(query)
    return str(response)

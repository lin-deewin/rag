# /home/lqp/projs/rag/mcp_server.py
from fastmcp import FastMCP
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# 初始化一个名为 Microeconomics-RAG 的 MCP 服务
mcp = FastMCP("Microeconomics-RAG")

# 1. 直接加载本地已有的 Chroma 数据库
# 注意：使用绝对路径确保 OpenCode 在任意目录下调用时都能找到数据库
DB_DIR = "/home/lqp/projs/rag/chroma_db"
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# 2. 注册为大模型可调用的工具
@mcp.tool()
def search_economics_textbook(query: str) -> str:
    """
    当用户问到有关微观经济学概念、教材中的特定逻辑、机会成本、供求关系等经济学专业问题时，
    调用此工具来检索本地经济学教材的相关文本段落。
    """
    docs = retriever.invoke(query)
    return "\n\n".join(doc.page_content for doc in docs)

if __name__ == "__main__":
    mcp.run()

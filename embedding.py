from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# 1. 初始化本地 Ollama 向量模型
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. 向量化并保存到本地目录 ./chroma_db
vector_store = Chroma.from_documents(
    documents=docs, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)
print("向量数据库构建完成并已持久化到本地！")

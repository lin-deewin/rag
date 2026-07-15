import zipfile
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 自定义纯本地 ePub 解析函数（避开 NLTK 网络请求和 Pandoc 依赖）
def load_epub_locally(file_path):
    documents = []
    with zipfile.ZipFile(file_path, 'r') as archive:
        for name in sorted(archive.namelist()):
            if name.endswith(('.html', '.xhtml', '.htm')):
                with archive.open(name) as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    # 过滤掉无用的网页标签
                    for element in soup(["script", "style", "meta"]):
                        element.extract()
                    text = soup.get_text(separator="\n").strip()
                    if text:
                        documents.append(Document(page_content=text, metadata={"source": file_path}))
    return documents

# 1. 加载并切分文档
print("正在本地解析 ePub 教材（完全离线）...")
raw_docs = load_epub_locally("economics.epub")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(raw_docs)
print(f"成功切分为 {len(docs)} 个文本块。")

# 2. 向量化并持久化
print("正在构建本地向量数据库...")
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma.from_documents(
    documents=docs, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 3. 初始化本地大模型
llm = ChatOllama(model="modelscope.cn/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF:latest", temperature=0.3)

# 4. 构建 LCEL RAG 链
system_prompt = (
    "你是一个专业的微观经济学助教。请根据以下提供的教材内容，严谨、有条理地回答学生的问题。\n"
    "如果内容中没有相关信息，请直接说“教材中未提及”，不要瞎编。\n\n"
    "已知教材内容:\n{context}"
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 5. 运行
print("\n--- 系统准备就绪 ---")
query = "什么是机会成本？请用教材里的逻辑解释。"
response = rag_chain.invoke(query)

print(f"问题: {query}\n")
print(response)

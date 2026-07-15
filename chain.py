from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. 初始化本地大模型
llm = Ollama(model="qwen2.5:7b", temperature=0.3)  # 低温度系数减少幻觉

# 2. 定制经济学专用的 Prompt 模板
template = """你是一个专业的微观经济学助教。请根据以下提供的教材内容，严谨、有条理地回答学生的问题。
如果内容中没有相关信息，请直接说“教材中未提及”，不要瞎编。

已知教材内容:
{context}

学生提问: {question}
助教解析："""

QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# 3. 组装 RAG 链
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}), # 每次检索最相关的3个片段
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

from langchain_community.document_loaders import UnstructuredEPubLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 加载《微观经济学原理》ePub 文件（请确保文件名对应）
loader = UnstructuredEPubLoader("economics.epub")
documents = loader.load()

# 2. 文本分块（保持原有的清爽切分策略）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len
)
docs = text_splitter.split_documents(documents)
print(f"成功将 ePub 教材切分为 {len(docs)} 个文本块。")

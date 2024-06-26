from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.storage import LocalFileStore
from langchain.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.getenv("OPENAI_EMBEDDING_DEPLOYMENT_NAME")
OPENAI_EMBEDDING_MODEL_NAME = os.getenv("OPENAI_EMBEDDING_MODEL_NAME")
OPENAI_EMBEDDING_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_EMBEDDING_DEPLOYMENT_ENDPOINT")
OPENAI_EMBEDDING_DEPLOYMENT_VERSION = os.getenv("OPENAI_EMBEDDING_DEPLOYMENT_VERSION")
OPENAI_EMBEDDING_API_KEY = os.getenv("OPENAI_EMBEDDING_API_KEY")

"""
# Azure OpenAI Embeddings
OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.environ["OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
OPENAI_EMBEDDING_MODEL_NAME = os.environ["OPENAI_EMBEDDING_MODEL_NAME"]
OPENAI_EMBEDDING_DEPLOYMENT_ENDPOINT = os.environ["OPENAI_EMBEDDING_DEPLOYMENT_ENDPOINT"]
OPENAI_EMBEDDING_DEPLOYMENT_VERSION = os.environ["OPENAI_EMBEDDING_DEPLOYMENT_VERSION"]
OPENAI_EMBEDDING_API_KEY = os.environ["OPENAI_EMBEDDING_API_KEY"]
"""
# Embedding
"""
embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL_NAME, chunk_size=1,
                              deployment=OPENAI_EMBEDDING_DEPLOYMENT_NAME,
                              openai_api_base=OPENAI_EMBEDDING_DEPLOYMENT_ENDPOINT,
                              openai_api_type='azure',
                              openai_api_version=OPENAI_EMBEDDING_DEPLOYMENT_VERSION,
                              openai_api_key=OPENAI_EMBEDDING_API_KEY,
                              request_timeout=30)

llm = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
        deployment_name=OPENAI_DEPLOYMENT_NAME,
        openai_api_version=OPENAI_DEPLOYMENT_VERSION,
        openai_api_key=OPENAI_API_KEY, verbose=True, 
        request_timeout=60, temperature=0.2)
"""
# Embeddings
embeddings = AzureOpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL_NAME, chunk_size=1, 
                              deployment=OPENAI_EMBEDDING_DEPLOYMENT_NAME,
                              azure_endpoint=OPENAI_EMBEDDING_DEPLOYMENT_ENDPOINT, 
                              openai_api_type='azure', 
                              openai_api_version=OPENAI_EMBEDDING_DEPLOYMENT_VERSION,
                              openai_api_key=OPENAI_EMBEDDING_API_KEY,
                              request_timeout=30)
if __name__ == "__main__":
    # Name of the file for index creation
    filename = "sampletext.txt"

    # that file should be inside training_docs
    filepath = os.path.join("./multiverse-chat-foundation/src/training-docs/uploaded/", filename)

    # TextLoader incase of .txt files
    loader = TextLoader(file_path=filepath)

    # PyPDFLoader incase of .pdf files
    # loader = PyPDFLoader(file_path=filepath)

    pages = loader.load_and_split()

    fs = LocalFileStore("./src/indexes/cache/")

    cache_embedder = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=embeddings,
        document_embedding_cache=fs,
        namespace=embeddings.model
    )

    db = FAISS.from_documents(documents=pages, embedding=embeddings)
    fname = filename.split(".")[0]
    db.save_local(f"./src/indexes", fname)
    print("Embeddings created successfully.")

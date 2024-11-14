import os
import pinecone
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import WebBaseLoader

from consts import INDEX_NAME

load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENVIRONMENT_REGION")
pc = pinecone.Pinecone(api_key=pinecone_api_key, environment=pinecone_env)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

print(f"Pinecone connected. Current environment: {pinecone_env}")


def ingest_docs():
    loader = ReadTheDocsLoader("langchain-docs/api.python.langchain.com/en/latest")

    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")
    # Chunk_overlap is used to ensure continuity of context between text chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("****Loading to vectorstore done ***")


def ingest_docs2() -> None:
    langchain_documents_base_urls = [
        "https://python.langchain.com/v0.2/docs/integrations/chat/",
        "https://python.langchain.com/v0.2/docs/integrations/llms/",
        "https://python.langchain.com/v0.2/docs/integrations/text_embedding/",
        "https://python.langchain.com/v0.2/docs/integrations/document_loaders/",
        "https://python.langchain.com/v0.2/docs/integrations/document_transformers/",
        "https://python.langchain.com/v0.2/docs/integrations/vectorstores/",
        "https://python.langchain.com/v0.2/docs/integrations/retrievers/",
        "https://python.langchain.com/v0.2/docs/integrations/tools/",
        "https://python.langchain.com/v0.2/docs/integrations/stores/",
        "https://python.langchain.com/v0.2/docs/integrations/llm_caching/",
        "https://python.langchain.com/v0.2/docs/integrations/graphs/",
        "https://python.langchain.com/v0.2/docs/integrations/memory/",
        "https://python.langchain.com/v0.2/docs/integrations/callbacks/",
        "https://python.langchain.com/v0.2/docs/integrations/chat_loaders/",
        "https://python.langchain.com/v0.2/docs/concepts/",
    ]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)

    for url in langchain_documents_base_urls[:1]:
        print(f"Processing URL: {url}")
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()

            split_docs = text_splitter.split_documents(docs)

            print(f"Going to add {len(split_docs)} documents to Pinecone")
            PineconeVectorStore.from_documents(
                split_docs, embeddings, index_name=INDEX_NAME
            )
            print(f"****Loading {url} to vectorstore done ***")
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")


if __name__ == "__main__":
    ingest_docs2()

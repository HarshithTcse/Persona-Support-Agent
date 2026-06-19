import os
from dotenv import load_dotenv
from google import genai
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

def load_documents(data_folder="data"):
    documents = []

    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)

        # Read Markdown and Text files
        if filename.endswith(".md") or filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            documents.append({
                "source": filename,
                "content": text
            })

        # Read PDF files
        elif filename.endswith(".pdf"):
            reader = PdfReader(filepath)

            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()

                documents.append({
                    "source": filename,
                    "page": page_num + 1,
                    "content": text
                })

    return documents
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=40
    )

    chunks = []

    for doc in documents:

        split_texts = splitter.split_text(doc["content"])

        for idx, text in enumerate(split_texts):

            chunks.append({
                "content": text,
                "source": doc["source"],
                "chunk_id": idx
            })

    return chunks

class LocalRAGPipeline:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.chroma_client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="support_kb"
        )

    def get_embedding(self, text):

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values

    def ingest_chunks(self, chunks):

        for i, chunk in enumerate(chunks):

            embedding = self.get_embedding(
                chunk["content"]
            )

            try:
                self.collection.add(
                    ids=[f"chunk_{i}"],
                    embeddings=[embedding],
                    documents=[chunk["content"]],
                    metadatas=[{
                        "source": chunk["source"]
                    }]
                )
            except:
                pass

        print("Knowledge Base Indexed Successfully")

    def retrieve_context(self, query, top_k=3):

        query_embedding = self.get_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_chunks = []

        for i in range(len(results["documents"][0])):

            retrieved_chunks.append({
                "content": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"]
            })

        return retrieved_chunks

if __name__ == "__main__":

    docs = load_documents()

    chunks = chunk_documents(docs)

    rag = LocalRAGPipeline()

    rag.ingest_chunks(chunks)

    query = "How do I reset my password?"

    results = rag.retrieve_context(query)

    print("\nRetrieved Chunks:\n")

    for item in results:
        print(item)
        print("-" * 24)
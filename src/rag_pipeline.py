import os
from dotenv import load_dotenv
from google import genai
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


def load_documents(data_folder="data"):
    documents = []

    if not os.path.exists(data_folder):
        print(f"Folder '{data_folder}' not found.")
        return documents

    for filename in os.listdir(data_folder):

        filepath = os.path.join(data_folder, filename)

        if filename.endswith(".txt") or filename.endswith(".md"):

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            documents.append({
                "source": filename,
                "content": text
            })

        elif filename.endswith(".pdf"):

            try:
                reader = PdfReader(filepath)

                for page_num, page in enumerate(reader.pages):

                    text = page.extract_text()

                    if text:
                        documents.append({
                            "source": filename,
                            "page": page_num + 1,
                            "content": text
                        })

            except Exception as e:
                print(f"Error reading PDF {filename}: {e}")

    return documents


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=40
    )

    chunks = []

    for doc in documents:

        split_texts = splitter.split_text(
            doc["content"]
        )

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

        self.collection = (
            self.chroma_client.get_or_create_collection(
                name="support_kb"
            )
        )

    def get_embedding(self, text):

        try:

            response = self.client.models.embed_content(
                model="gemini-embedding-001",
                contents=text
            )

            if response.embeddings:
                return response.embeddings[0].values

            return []

        except Exception as e:

            print(f"Embedding Error: {e}")
            return []

    def ingest_chunks(self, chunks):

        for i, chunk in enumerate(chunks):

            embedding = self.get_embedding(
                chunk["content"]
            )

            if not embedding:
                continue

            try:

                self.collection.add(
                    ids=[
                        f"{chunk['source']}_{i}"
                    ],
                    embeddings=[embedding],
                    documents=[
                        chunk["content"]
                    ],
                    metadatas=[{
                        "source": chunk["source"]
                    }]
                )

            except Exception:
                continue

        print("Knowledge Base Indexed Successfully")

    def retrieve_context(
        self,
        query,
        top_k=3
    ):

        query_embedding = self.get_embedding(
            query
        )

        if not query_embedding:
            return []

        try:

            results = self.collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=top_k
            )

            if not results["documents"]:
                return []

            retrieved_chunks = []

            for i in range(
                len(results["documents"][0])
            ):

                retrieved_chunks.append({
                    "content":
                    results["documents"][0][i],

                    "source":
                    results["metadatas"][0][i]["source"]
                })

            return retrieved_chunks

        except Exception as e:

            print(f"Retrieval Error: {e}")
            return []


if __name__ == "__main__":

    docs = load_documents()

    print(
        f"Loaded {len(docs)} documents"
    )

    chunks = chunk_documents(docs)

    print(
        f"Created {len(chunks)} chunks"
    )

    rag = LocalRAGPipeline()

    if rag.collection.count() == 0:

        rag.ingest_chunks(chunks)

    query = (
        "How do I reset my password?"
    )

    results = rag.retrieve_context(
        query
    )

    print("\nRetrieved Chunks:\n")

    for item in results:

        print(
            f"Source: {item['source']}"
        )

        print(item["content"])

        print("-" * 50)

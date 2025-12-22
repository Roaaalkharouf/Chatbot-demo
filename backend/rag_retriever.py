import json
import boto3
import numpy as np
from typing import List, Dict

AWS_REGION = "eu-central-1"
EMBED_MODEL = "amazon.titan-embed-text-v2:0"

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# Embed text with Titan embeddings
def embed_text(text: str) -> np.ndarray:
    body = {"inputText": text}
    response = bedrock.invoke_model(
        modelId=EMBED_MODEL,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )
    result = json.loads(response["body"].read())
    return np.array(result["embedding"], dtype=float)


# RAG RETRIEVER
class RAGRetriever:
    def __init__(self, kb_path: str):
        print(f"Loading knowledge base from {kb_path}")
        
        with open(kb_path, "r") as f:
            raw_data = json.load(f)

        # Convert website pages to retrievable chunks
        self.chunks = self._chunk_all_pages(raw_data)
        print("Total chunks created:", len(self.chunks))

        # Create embeddings for all chunks
        self.embeddings = np.array([embed_text(c["content"]) for c in self.chunks])
        print("Embeddings created successfully.")

    # FIXED: chunking function exists AND supports list values
    def _chunk_all_pages(self, raw_dict: Dict[str, str]) -> List[Dict]:
        chunks = []
        CHUNK_SIZE = 140  # ~100–140 words per chunk

        for url, text in raw_dict.items():

            # FIX: If text is a list, merge it
            if isinstance(text, list):
                text = " ".join([str(t) for t in text])

            words = text.split()
            for i in range(0, len(words), CHUNK_SIZE):
                piece = " ".join(words[i:i + CHUNK_SIZE])
                if len(piece.strip()) > 0:
                    chunks.append({
                        "section": url,
                        "content": piece
                    })
        
        return chunks

    # Retrieve relevant chunks
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        print(f"Searching for: {query}")

        # Embed the query
        query_emb = embed_text(query)

        # Cosine similarity
        scores = np.dot(self.embeddings, query_emb) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_emb)
        )

        # Best matches
        top_idxs = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_idxs:
            results.append({
                "section": self.chunks[idx]["section"],
                "content": self.chunks[idx]["content"],
                "score": float(scores[idx])
            })

        return results

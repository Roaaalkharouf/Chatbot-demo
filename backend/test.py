from rag_retriever import RAGRetriever
from bedrock_client import call_model

retriever = RAGRetriever("cirrusgo_cleaned.json")

def ask(q):
    context = retriever.retrieve(q)
    prompt = {"history": [], "context": context, "question": q}
    print(call_model("titan", prompt))

ask("Give me more information about cirrusgo?")

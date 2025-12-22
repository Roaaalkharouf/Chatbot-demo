import json
from rag_retriever import RAGRetriever
from bedrock_client import call_model
from moderation import is_inappropriate
from memory import SessionMemory

# Initialize once (cold start)
retriever = RAGRetriever("cirrusgo_cleaned.json")
memory = SessionMemory()

def lambda_handler(event, context=None):
    # ------------------------------------
    # Handle Function URL JSON body
    # ------------------------------------
    if "body" in event and isinstance(event["body"], str):
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError:
            body = {}
    else:
        body = event
    

    user_message = body.get("user_message", "")
    session_id = body.get("session_id", "default")
    model_name = body.get("model", "titan")

    if not user_message:
        return respond("No user message provided.")

    # Moderation
    if is_inappropriate(user_message):
        return respond("⚠️ This topic cannot be discussed.")

    # Conversation memory
    history = memory.get_history(session_id)

    # RAG retrieval
    context_chunks = retriever.retrieve(user_message)

    # Prompt for model
    prompt = {
        "history": history,
        "context": context_chunks,
        "question": user_message
    }

    # Call Bedrock model
    answer = call_model(model_name, prompt)

    # Save memory
    memory.add_message(session_id, "user", user_message)
    memory.add_message(session_id, "assistant", answer)

    return respond(answer)

def respond(message: str):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"response": message})
    }

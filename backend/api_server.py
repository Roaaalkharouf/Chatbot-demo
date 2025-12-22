from fastapi import FastAPI
from pydantic import BaseModel
import json
from lambda_handler import lambda_handler
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_message: str
    session_id: str | None = "demo-session"
    model: str | None = "claude"

@app.get("/")
def home():
    return {"message": "Cirrusgo Chatbot Backend is Running"}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    event = {
        "user_message": req.user_message, #user_message=hello
        "session_id": req.session_id, #session_id=abc
        "model": req.model, #model=titan or claude 
    }

    result = lambda_handler(event)

    body = result.get("body", "{}")
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"response": body}

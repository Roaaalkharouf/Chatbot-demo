import os
import json
import boto3
from typing import Dict, List


# Bedrock client
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1") 

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# Double-check these model IDs in the Bedrock console for your region.
CLAUDE_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
TITAN_MODEL_ID  = "amazon.titan-text-express-v1"

# Helper: build a single text prompt from our structured object
def build_prompt(prompt: Dict) -> str:
    """
    Convert {history, context, question} into a single text prompt
    that we send to the model.
    """
    history: List[Dict] = prompt.get("history", [])
    context_chunks: List[Dict] = prompt.get("context", [])
    question: str = prompt.get("question", "")

    history_text = ""
    for turn in history:
        role = turn.get("role", "user")
        content = turn.get("content", "")
        history_text += f"{role.upper()}: {content}\n"

    context_text = ""
    for c in context_chunks:
        section = c.get("section", "")
        content = c.get("content", "")
        context_text += f"[{section}] {content}\n"

    final_prompt = f"""
You are Cirrusgo’s official AI assistant.
You may answer general identity or greeting questions using your assistant role.
For company-related questions, answer strictly using the provided context.


CONTEXT:
{context_text}

CONVERSATION SO FAR:
{history_text}

USER QUESTION:
{question}

Provide a clear, concise answer, in a professional tone.
"""
    return final_prompt.strip()


# Claude 3.5 via Bedrock (Anthropic)
import os
import json
import boto3
from typing import Dict, List

# Bedrock client
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")  # change if needed

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

CLAUDE_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
TITAN_MODEL_ID  = "amazon.titan-text-express-v1"


# Helper: build a single text prompt from our structured object
def build_prompt(prompt: Dict) -> str:
    """
    Convert {history, context, question} into a single text prompt
    that we send to the model.
    """
    history: List[Dict] = prompt.get("history", [])
    context_chunks: List[Dict] = prompt.get("context", [])
    question: str = prompt.get("question", "")

    history_text = ""
    for turn in history:
        role = turn.get("role", "user")
        content = turn.get("content", "")
        history_text += f"{role.upper()}: {content}\n"

    context_text = ""
    for c in context_chunks:
        section = c.get("section", "")
        content = c.get("content", "")
        context_text += f"[{section}] {content}\n"

    final_prompt = f"""
You are an AI assistant for Cirrusgo, an AWS and cloud consulting company.
Answer ONLY using information that is consistent with the context below.
If you are not sure, say that the information is not available.

CONTEXT:
{context_text}

CONVERSATION SO FAR:
{history_text}

USER QUESTION:
{question}

Provide a clear, concise answer, in a professional tone.
"""
    return final_prompt.strip()


# Claude 3.5 via Bedrock (Anthropic)
def call_claude(prompt: Dict) -> str:
    prompt_text = build_prompt(prompt)

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text}
                ],
            }
        ],
        "max_tokens": 512,
        "temperature": 0.5,
    }

    response = bedrock.invoke_model(
        modelId=CLAUDE_MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )

    result = json.loads(response["body"].read())
    # Claude returns a list of content blocks; take the first text block
    text = ""
    for block in result.get("content", []):
        if block.get("type") == "text":
            text += block.get("text", "")
    return text.strip()


# Titan Text via Bedrock (Amazon)
def call_titan(prompt: Dict) -> str:
    prompt_text = build_prompt(prompt)

    body = {
        "inputText": prompt_text,
        "textGenerationConfig": {   
            "maxTokenCount": 512,
            "temperature": 0.3,
            "topP": 0.9
        }
    }

    response = bedrock.invoke_model(
        modelId=TITAN_MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    
    outputs = result.get("results", [])
    if not outputs:
        return "Model did not return any text."

    return outputs[0].get("outputText", "").strip()


# Unified entry used by lambda_handler.py
def call_model(model_name: str, prompt: Dict) -> str:
    model_name = model_name.lower()

    if model_name == "claude":
        return call_claude(prompt)

    if model_name == "titan":
        return call_titan(prompt)

    # Default fallback
    return call_claude(prompt)

# Titan Text via Bedrock (Amazon)
def call_titan(prompt: Dict) -> str:
    prompt_text = build_prompt(prompt)

    body = {
        "inputText": prompt_text,
        "textGenerationConfig": {   
            "maxTokenCount": 512,
            "temperature": 0.3,
            "topP": 0.9
        }
    }

    response = bedrock.invoke_model(
        modelId=TITAN_MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    
    outputs = result.get("results", [])
    if not outputs:
        return "Model did not return any text."

    return outputs[0].get("outputText", "").strip()


# Unified entry used by lambda_handler.py
def call_model(model_name: str, prompt: Dict) -> str:
    model_name = model_name.lower()

    if model_name == "claude":
        return call_claude(prompt)

    if model_name == "titan":
        return call_titan(prompt)

    # Default fallback
    return call_claude(prompt)

from fastapi import FastAPI
from pydantic import BaseModel
from src.services.llm_router import llm_routing

app = FastAPI(
    title="LLM Router API",
    description="Routes user messages to the appropriate LLM handler (general, specific, tool call).",
    version="1.0.0",
)

# Request body schema
class MessageRequest(BaseModel):
    user_message: str

# Check API
@app.get("/")
def root():
    return {"message": "LLM Router API is running"}

# Endpoint to handle user messages
@app.post("/route")
def route_message(request: MessageRequest):
    response = llm_routing(request.user_message, llm="llama") # Select llm model first
    return {"response": response}
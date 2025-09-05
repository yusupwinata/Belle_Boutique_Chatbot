import os
import google.generativeai as genai
from typing import Literal
from dotenv import load_dotenv
from openai import OpenAI
from src.services.inference import answer_general_question
from src.services.rag import answer_specific_question
from src.services.tools_calls import answer_tool_request

# Models configurations
api_key_ollama= "ollama"
base_url_ollama = "http://localhost:11434/v1"
client_ollama = OpenAI(base_url=base_url_ollama, api_key=api_key_ollama)
model_ollama = "llama3.2"

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_gpt = OpenAI(api_key=OPENAI_API_KEY)
model_gpt = "gpt-4o-mini"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model_google = genai.GenerativeModel("gemini-2.0-flash")

# Prompting
system_message = """You are a routing assistant that decides how to handle a user's message by selecting one of three categories. Your job is to analyze the user's message and respond with only one of the following routing labels:
- general_question: For greetings, casual conversation, or common knowledge questions (e.g., "Hello", "What's the weather?", "Tell me a joke").
- specific_question: For questions that require information related to company details, product catalog, services, or FAQs (e.g., "What products do you offer?", "Tell me about your company").
- tool_calls: For messages that require executing a specific action using a tool or API, such as checking order or shipping status, booking a service, or retrieving real-time data (e.g., "Track my order", "Check my booking").

Respond with only the label: "general_question", "specific_question", or "tool_calls".
Do not explain your choice or include any other text."""

def llm_routing(user_message: str, llm: Literal["llama", "gpt", "gemini"] = "gpt") -> str:
    # LLM Selection
    if llm == "llama":
        print("Llama3.2 selected")
        modified_user_message = "\n\nSelect a category for this user's message:\n"
        modified_user_message += user_message
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": modified_user_message}
        ]

        response = client_ollama.chat.completions.create(
            model=model_ollama,
            messages=messages,
            temperature=0.7
        )
        route = response.choices[0].message.content.strip()

    elif llm == "gpt":
        print("GPT 4.0 mini selected")
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        response = client_gpt.chat.completions.create(
            model=model_gpt,
            messages=messages,
            temperature=0.7
        )
        route = response.choices[0].message.content.strip()

    elif llm == "gemini":
        print("Gemini Flash 2.0 selected")
        prompt = (
            system_message
            + "\n\nSelect a category for this user's message:\n"
            + user_message
        )

        response = model_google.generate_content(prompt)
        route = response.text.strip()

    else:
        print("Error while selecting LLM: model unknown")
        route = "Unknown"
    
    print(f"Route: {route}")

    # Routing
    if route == "general_question":
        response = answer_general_question(user_message=user_message)
    elif route == "specific_question":
        response = answer_specific_question(user_message=user_message)
    elif route == "tool_calls":
        response = answer_tool_request(user_message=user_message)
    else:
        print("Error while routing using LLM: route unknown")
        response = "Unknown"
    
    print(response)
    
    return response

if __name__ == "__main__":
    questions = [
        "halo",
        "apa kelebihan produk eleganza?",
        "bagaimana cara saya meng-claim garansi?",
        "dimana pesanan saya?",
        "cek nomor resi RESI00008ID",
        "dimana pesanan saya dengan nomor resi RESI00005ID"
    ]
    
    test = llm_routing(user_message=questions[4], llm="llama")
    print(f"{type(test)}: {test}")
from openai import OpenAI
from src.storage.sql import SQL
from src.services.generate_messages import generate_messages

# Model settings
base_url = 'http://localhost:11434/v1'
api_key='ollama'
client = OpenAI(base_url=base_url, api_key=api_key)
model = "llama3.2"

# Prompting
system_message ="Kamu adalah asisten yang sangat membantu. Jawab pertanyaan user dengan sopan dan singkat"

def answer_general_question(user_message: str) -> str:
    # Get chat history from database
    database = SQL()
    messages = generate_messages(
        system_message=system_message,
        chat_history=database.get_chat_history(),
        new_user_message=user_message,
    )
    # print(f"\nChat History:\n{messages}")

    # Generate response
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1
    )
    assistant_message = response.choices[0].message.content
    # print(f"\nResponse:\n{assistant_message}")

    # Save chat history to database
    database.save_chat_history(
        user_message=user_message,
        assistant_message=assistant_message
    )
    
    return assistant_message

if __name__ == "__main__":
    test = answer_general_question(user_message="kamu apa kabar?")
    print(f"{type(test)}: {test}")
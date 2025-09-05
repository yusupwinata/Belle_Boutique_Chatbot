from openai import OpenAI
from src.storage.sql import SQL
from src.storage.vectorstore import Vectorstore
from src.services.generate_messages import generate_messages

# Model settings
base_url = 'http://localhost:11434/v1'
api_key='ollama'
client = OpenAI(base_url=base_url, api_key=api_key)
model = "llama3.2"

# Prompting
system_message ="Jawab pertanyaan user dengan singkat dan detail"

def answer_specific_question(user_message: str) -> str:
    # Get relevant document
    vectorstore = Vectorstore(embeddings_model="nomic") # Select embeddings model first
    knowledge = vectorstore.similarity_search(query=user_message)

    rag_user_message = f"Konteks:\n{knowledge}"
    rag_user_message += f"\n\nPertanyaan:\n{user_message}"
    # print(f"{rag_user_message}")

    # Get chat history from database
    database = SQL()
    messages = generate_messages(
        system_message=system_message,
        chat_history=database.get_chat_history(),
        new_user_message=rag_user_message,
    )
    # print(f"\nChat History:\n{messages}")

    # Generate response
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
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
    test = answer_specific_question(user_message="kelebihan tote bag")
    print(f"{type(test)}: {test}")
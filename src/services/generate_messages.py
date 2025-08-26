import pandas as pd

def generate_messages(new_user_message: str, chat_history: pd.DataFrame, system_message: str =""):
    messages = []
    
    if system_message:
        messages.append({"role": "system", "content": system_message})

    if not chat_history.empty:
        for _, chat in chat_history[::-1].iterrows():
            messages.append({"role": "user", "content": chat["user_message"]})
            messages.append({"role": "assistant", "content": chat["assistant_message"]})

    messages.append({"role": "user", "content": new_user_message})

    return messages
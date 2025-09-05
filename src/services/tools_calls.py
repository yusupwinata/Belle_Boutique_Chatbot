import json
from openai import OpenAI
from src.storage.sql import SQL
from src.services.generate_messages import generate_messages

# Model settings
base_url = 'http://localhost:11434/v1'
api_key='ollama'
client = OpenAI(base_url=base_url, api_key=api_key)
model = "llama3.2"

# Data
database = None

# Tools
def get_shipping_status(tracking_number: str) -> dict:
    shipping_status = database.get_order_status(nomor_resi=tracking_number)
    return shipping_status

# Tools descriptions
get_shipping_status_function = {
    "name": "get_shipping_status",
    "description": "Retrieve the current shipping status based on the tracking number. This function queries the database to get the latest order status using the provided tracking number. Use this when a customer or internal team member wants to track the status of a shipment.",
    "parameters": {
        "type": "object",
        "properties": {
            "tracking_number": {
                "type": "string",
                "description": "The unique shipping tracking number (nomor resi). Example: 'RESI00005ID'"
            }
        },
        "required": ["tracking_number"],
        "additionalProperties": False
    }
}

# Tools calling
def handle_tool_calls(tool_message):
    responses = []

    for tool_call in tool_message.tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments) # extract arguments from user input

        if tool_name == "get_shipping_status":
            tracking_number = arguments.get("tracking_number")
            if tracking_number:
                content = get_shipping_status(tracking_number=tracking_number)
            else:
                content = {"warning": f"please input tracking number or nomor resi"}
        else:
            content = {"error": f"unknown tool: {tool_name}"}
        
        responses.append({
            "role": "tool",
            "content": json.dumps(content),
            "tool_call_id": tool_call.id
        })

    return responses

# Prompting
system_message ="Jawab pertanyaan user dengan singkat dan detail"

def answer_tool_request(user_message: str) -> str:
    # Get chat history from database
    global database
    database = SQL()
    messages = generate_messages(
        system_message=system_message,
        chat_history=database.get_chat_history(),
        new_user_message=user_message,
    )
    # print(f"\nChat History:\n{messages}")

    # Get available tools
    tools = [{"type": "function", "function": get_shipping_status_function}]

    # Generate response and reasoning
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        temperature=0.3
    )

    # Generate response by using tools
    if response.choices[0].finish_reason == "tool_calls":
        tool_message = response.choices[0].message
        tool_responses = handle_tool_calls(tool_message=tool_message)

        messages.append(tool_message)
        messages.extend(tool_responses)
        # print(f"\nTools Response:\n{tool_responses}")
        # print(f"\nMessages:\n{messages}")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3
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
    test = answer_tool_request(user_message="cek nomor resi RESI00008ID") # cek nomor resi RESI00009ID
    print(f"{type(test)}: {test}")
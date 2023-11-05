import json
import openai
from weather_api import get_current_weather

openai.api_base = 'https://api.ngapi.top/v1'

def save_to_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)
    return {"status": "success", "message": f"Content saved to {filename}"}

def callGpt(model, systemPrompt, userPrompt):
    def call_function(function_name, args):
        available_functions = {
            "get_current_weather": get_current_weather,
            "save_to_file": save_to_file
        }
        function_to_call = available_functions[function_name]
        return function_to_call(**args)

    messages = [
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": userPrompt}
    ]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city, e.g. Shanghai"},
                    "unit": {"type": "string", "enum": ["metric"]},
                },
                "required": ["location"],
            },
        },
        {
            "name": "save_to_file",
            "description": "Save content to a TXT file",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The content to save"},
                    "filename": {"type": "string", "description": "The name of the file"},
                },
                "required": ["content", "filename"],
            },
        }
    ]

    while True:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        print(response)
        response_message = response['choices'][0]['message']
        finish_reason = response['choices'][0]['finish_reason']

        messages.append(response_message)

        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = call_function(function_name, function_args)

            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(function_response),
                }
            )

        if finish_reason == 'stop':
            print(messages)
            return response_message['content']

# Example usage:
systemPrompt = "You are a helpful assistant."
userPrompt = "Is the weather sunnier in Shanghai than Chengdu? Can you give me both the weather of Shanghai and Chengdu, and save the result to a file?"
print(callGpt("gpt-4-0613", systemPrompt, userPrompt))


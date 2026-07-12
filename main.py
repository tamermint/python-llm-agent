import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
import json
from prompts import system_prompt
from call_function import available_functions


def chatWithAI():
    try:
        load_dotenv()
        api_key = os.environ.get("OPENROUTER_API_KEY")
        client = OpenAI(    
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        parser = argparse.ArgumentParser(description="LLM Chatbot")
        parser.add_argument("user_prompt", type=str, help="User prompt")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
        args = parser.parse_args()

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ]

        response = client.chat.completions.create(
            model="openrouter/free", 
            messages=messages, 
            tools=available_functions
        )
        if response.usage is None:
            raise RuntimeError("No usage indicated! Check API parametres")
        prompt_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens
        message_tool_calls = response.choices[0].message.tool_calls
        if(args.verbose):
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            print(response.choices[0].message.content)
        elif(message_tool_calls):
            for tool_call in message_tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
        else:
            print(response.choices[0].message.content)
    except Exception as e:
        print(f"Unknown error occured: {e}")


def main():
    chatWithAI()
if __name__ == "__main__":
    main()

import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse


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
                "role": "user",
                "content": args.user_prompt,
            }
        ]

        response = client.chat.completions.create(model="openrouter/free", messages=messages)
        if response.usage is None:
            raise RuntimeError("No usage indicated! Check API parametres")
        prompt_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens
        if(args.verbose):
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            print(response.choices[0].message.content)
        else:
            print(response.choices[0].message.content)
    except Exception as e:
        print(f"Unknown error occured: {e}")


def main():
    chatWithAI()
if __name__ == "__main__":
    main()

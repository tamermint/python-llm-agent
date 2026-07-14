import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function


def ai_assistant_agent(client: OpenAI, messages: list, verbose: bool):
    response = client.chat.completions.create(
        model="openrouter/free", 
        messages=messages, 
        tools=available_functions
    )
    
    if not response.usage:
        raise RuntimeError("No usage indicated! Check API parametres")
    
    if(verbose):
        print(f"Prompt tokens: {response.usage.prompt_tokens}\n")
        print(f"Response tokens: {response.usage.completion_tokens}\n")

    message = response.choices[0].message
    messages.append(message)
        
    if(message.tool_calls):
        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                continue
            result_message = call_function(tool_call, verbose)
            if(not result_message["content"]):
                raise RuntimeError(f"No content returned for {tool_call.function.name}!")
            if verbose: 
                print(f"-> {result_message['content']}")
            if not verbose:
                print(result_message['content'])
            messages.append(result_message)
    else:
        print("Final Response:\n")
        print(message.content)
        return 1


def main():
    try:
        load_dotenv()
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY environment variable is not set or missing value")

        client = OpenAI(    
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        parser = argparse.ArgumentParser(description="AI Code Assistant")
        parser.add_argument("user_prompt", type=str, help="Prompt to send to LLM")
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

        if args.verbose:
            print(f"User prompt: {args.user_prompt}\n")

        for _ in range (20):
            try:
                output = ai_assistant_agent(client, messages, args.verbose)
                if output == 1:
                    break
            except Exception as e:
                print(f"Error occured: {e}")
                break
        else:
            exit(1)

    except Exception as e:
        return f"Unknown error occured:{e}"

if __name__ == "__main__":
    main()

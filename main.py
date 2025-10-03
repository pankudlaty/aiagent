import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    load_dotenv()
    args = sys.argv[1:]
    if not args:
        print("AI Code Assistant")
        print("\nUsage: python main.py [user_prompt]")
        sys.exit(1)
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    generate_content(client, messages)


def generate_content(client, messages):
    respone = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )
    print(respone.text)
    print(f"Prompt tokens: {respone.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {respone.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()

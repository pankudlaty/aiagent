from re import escape
import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from available_functions import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "user_prompt" [--verbose]')
        sys.exit(1)
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    iters = 0
    while True:
        iters += 1
        if iters > 20:
            print(f"Max iterations (20) reached.")
            sys.exit(1)

        try:
            fin_resp = generate_content(client, messages, verbose)
            if fin_resp:
                print("Final response")
                print(fin_resp)
                break
        except Exception as e:
            print(f"Error in generate content: {e}")


def generate_content(client, messages, verbose):

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.candidates:
        for cand in response.candidates:
            func_call_content = cand.content
            messages.append(func_call_content)
    if not response.function_calls:
        return response.text

    func_resp = []
    for func_call_part in response.function_calls:
        func_call_result = call_function(func_call_part, verbose)
        if (
            not func_call_result.parts
            or not func_call_result.parts[0].function_response
        ):
            raise Exception("empyt function call result")
        if verbose:
            print(f"-> {func_call_result.parts[0].function_response.response}")
        func_resp.append(func_call_result.parts[0])

    messages.append(types.Content(role="user", parts=func_resp))


if __name__ == "__main__":
    main()

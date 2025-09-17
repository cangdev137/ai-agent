import os
import sys
from dotenv import load_dotenv
from google import genai
from prompts import system_prompt
from functions.available_functions import available_functions

#get response from ai agent
def get_response(client, user_prompt, verbose=False):
    #record message history
    messages = [ genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]), ]
    response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages, 
            config=genai.types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    #format agent response
    agent_response_parts = []
    if verbose:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        agent_response_parts.append(f"User prompt: {prompt}")
        agent_response_parts.append(f"Prompt tokens: {prompt_tokens}")
        agent_response_parts.append(f"Response tokens: {response_tokens}")
    if response.function_calls and len(response.function_calls) > 0:
        for function_call in response.function_calls:
            agent_response_parts.append(f"Calling function: {function_call.name}({function_call.args})")
    else:
        agent_response_parts.append(response.text)
    return "\n".join(agent_response_parts)


def main():
    load_dotenv()

    #toggle verbose mode if needed. don't include flag in user prompt
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")

    #get user prompt for agent
    user_prompt = ""
    if len(sys.argv) > 1:
        user_prompt = "".join(sys.argv[1:])
    else:
        print("Error: please provide a prompt.")
        print("Example usage: python3 main \"What day is it?\" [--verbose]")
        sys.exit(1)
        
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    agent_response = get_response(client, user_prompt, verbose)
    print(agent_response)

if __name__ == "__main__":
    main()


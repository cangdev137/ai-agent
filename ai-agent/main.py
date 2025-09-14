import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
def main():
    #gemini configuration
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"

    #toggle verbose mode if needed. don't include flag in user prompt
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")

    #get user prompt for agent
    prompt = ""
    if len(sys.argv) > 1:
        prompt = "".join(sys.argv[1:])
    else:
        print("Error: please provide a prompt.")
        print("Example usage: HeyAgent \"What day is it?\" [--verbose]")
        sys.exit(1)
        
    #hold conversation history 
    messages = [ genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)]), ]

    response = client.models.generate_content(model=model, contents=messages)
    print(response.text)

    if verbose:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()

import os
import sys
from dotenv import load_dotenv
from google import genai
from config import WORKING_DIR
from prompts import system_prompt
from functions.available_functions import available_functions, function_map

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function {function_call_part.name}({function_call_part.args})", end="")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_result = None
        
    if function_name in function_map:
        kwargs = dict(function_call_part.args)
        #add working directory manually
        kwargs["working_directory"] = WORKING_DIR
        function_result = function_map[function_name](**kwargs)

    response = {"result": function_result} if function_result else {"error": f"Unknown function: {function_name}"}
    return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_name,
                    response=response,
                )
            ],
    )


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

        agent_response_parts.append(f"User prompt: {user_prompt}")
        agent_response_parts.append(f"Prompt tokens: {prompt_tokens}")
        agent_response_parts.append(f"Response tokens: {response_tokens}")

    if not response.function_calls:
        agent_response_parts.append(response.text)
        return "\n".join(agent_response_parts)
    
    function_call_results = []
    for function_call_parts in response.function_calls:
            function_call_result = call_function(function_call_parts, verbose)

            if not function_call_result.parts or not function_call_result.parts[0].function_response:
                raise Exception("Error: function call produced no result")

            if verbose:
                print(f" -> {function_call_result.parts[0].function_response.response}")

            function_call_results.append(function_call_result.parts[0])

    if not function_call_results:
        return Exception("FATAL: all function calls failed to produce a result.")

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
        

if __name__ == "__main__":
    main()


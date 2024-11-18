# src/api/llm_parser.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_results_with_llm(entity, web_results, user_prompt):
    """
    Uses OpenAI's GPT API to extract information from web search results.
    
    Args:
        entity (str): The entity name (e.g., company name).
        web_results (dict): The web search results.
        user_prompt (str): The custom prompt provided by the user.

    Returns:
        str: Extracted information or error message.
    """
    try:
        # Format the web results
        formatted_results = "\n".join([f"- {result.get('snippet', '')}" for result in web_results.get('organic_results', [])])
        prompt = f"{user_prompt.replace('{company}', entity)}\n\nWeb Results:\n{formatted_results}"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error with LLM API: {e}")
        return "Error: Unable to extract information using LLM."

"""
Utility functions for LLM calls and helper functions.
"""
import os
from openai import OpenAI

def call_llm(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    """
    Call an LLM with a prompt and return the response.

    Args:
        prompt: The prompt to send to the LLM
        model: The model to use (default: gpt-4o-mini)
        temperature: Temperature for response randomness

    Returns:
        The LLM's response as a string
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )

    return response.choices[0].message.content


def format_persona_output(persona_name: str, thinking: str, output: str) -> dict:
    """
    Format a persona's output in a consistent way.

    Args:
        persona_name: Name of the persona
        thinking: The persona's reasoning process
        output: The persona's final output

    Returns:
        Formatted dictionary with persona output
    """
    return {
        "persona": persona_name,
        "thinking": thinking,
        "output": output
    }


def extract_yaml_from_response(response: str) -> str:
    """
    Extract YAML content from markdown code blocks.

    Args:
        response: The response containing YAML

    Returns:
        Extracted YAML string
    """
    if "```yaml" in response:
        return response.split("```yaml")[1].split("```")[0].strip()
    elif "```" in response:
        return response.split("```")[1].split("```")[0].strip()
    return response.strip()


# Test the LLM connection
if __name__ == "__main__":
    print("Testing LLM connection...")
    response = call_llm("Say 'Hello from Myfrendo!' in a friendly way.")
    print(f"Response: {response}")
    print("✅ LLM connection successful!")

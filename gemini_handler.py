import os
import google.generativeai as genai
import json
import logging

# Use the latest Gemini 2.5 Pro model
GEMINI_MODEL = "models/gemini-2.5-pro"

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# You must set your Gemini API key as an environment variable: GEMINI_API_KEY

def load_prompt_template() -> str:
    template_path = os.path.join(os.path.dirname(__file__), 'prompt_template.txt')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_with_gemini(file_tree: str, file_contents: dict, readme: str) -> dict:
    prompt = load_prompt_template()
    prompt = prompt.replace('{{file_tree}}', file_tree)
    prompt = prompt.replace('{{file_contents}}', json.dumps(file_contents)[:4000])
    prompt = prompt.replace('{{readme}}', readme or "(none)")
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.error('GEMINI_API_KEY environment variable not set.')
        raise EnvironmentError('GEMINI_API_KEY environment variable not set.')
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        logger.info(f"Gemini raw response: {response.text}")
        # Try to extract JSON from the response
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON substring
            import re
            match = re.search(r'\{[\s\S]*\}', response.text)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception as e:
                    logger.error(f"Failed to parse JSON substring: {e}")
            logger.error('Could not parse Gemini response as JSON')
            raise ValueError('Could not parse Gemini response as JSON')
    except Exception as e:
        logger.error(f"Gemini API call failed: {e}")
        raise 
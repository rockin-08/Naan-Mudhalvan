import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# List of preferred model names to support various Gemini API versions
CANDIDATE_MODELS = [
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash",
    "models/gemini-pro"
]

def _get_configured_genai():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
        genai.configure(api_key=api_key)
        return True
    return False

def answer_question_with_gemini(question: str) -> str:
    if not _get_configured_genai():
        return (
            f"💡 (Demo Mode - Please set your GEMINI_API_KEY in .env to use live Gemini AI)\n\n"
            f"Here is a helpful response to your question:\n"
            f"'{question}'\n\n"
            f"For example, if you asked about oceans: The Pacific Ocean is the largest ocean on Earth, "
            f"covering more than 30% of the Earth's surface."
        )

    last_error = None
    for model_name in CANDIDATE_MODELS:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(question)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            elif hasattr(response, "parts") and response.parts:
                return response.parts[0].text.strip()
        except Exception as e:
            last_error = e
            continue

    return f"⚠️ Error in QnA: {last_error}"

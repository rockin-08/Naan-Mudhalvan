import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

CANDIDATE_MODELS = [
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash",
    "models/gemini-pro"
]

def summarize_text(text: str) -> str:
    """Summarizes text into concise, easy-to-understand key points."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        # Fallback informative summary for testing
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 10]
        if sentences:
            concise = ". ".join(sentences[:2]) + "."
        else:
            concise = text[:150]
        return (
            f"Summary:\n\n{concise}\n\n"
            f"💡 Note: To get comprehensive Gemini generative summaries, set your GEMINI_API_KEY in the .env file."
        )

    genai.configure(api_key=api_key)
    prompt = f"Summarize the following text in simple, clear language for a student, retaining key facts and takeaways:\n\n{text}"

    last_error = None
    for model_name in CANDIDATE_MODELS:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
        except Exception as e:
            last_error = e
            continue

    return f"⚠️ Error in Summary: {last_error}"

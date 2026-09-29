import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Global holders for optional local model
explain_tokenizer = None
explain_model = None
_model_load_attempted = False

def _init_local_model():
    """Attempt to load MBZUAI/LaMini-Flan-T5-783M if transformers and torch are available."""
    global explain_tokenizer, explain_model, _model_load_attempted
    if _model_load_attempted:
        return explain_tokenizer, explain_model
    _model_load_attempted = True
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        print("Loading local explanation model: MBZUAI/LaMini-Flan-T5-783M...")
        explain_tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
        explain_model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
        print("MBZUAI/LaMini-Flan-T5-783M loaded successfully.")
    except Exception as e:
        print(f"Info: Local LaMini model not initialized ({e}). Using Gemini for explanations.")
        explain_tokenizer = None
        explain_model = None
    return explain_tokenizer, explain_model

def explain_topic(topic: str) -> str:
    """
    Explains the concept in a simple and clear way for a school student.
    Uses LaMini-Flan-T5 local model if available, otherwise uses Gemini.
    """
    tokenizer, model = _init_local_model()

    if tokenizer is not None and model is not None:
        try:
            input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            inputs = tokenizer(input_text, return_tensors="pt")
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )
            explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return explanation
        except Exception as e:
            print(f"Local model generation failed: {e}. Falling back to Gemini.")

    # Gemini AI fallback
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
        genai.configure(api_key=api_key)
        for model_name in [
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-flash",
            "models/gemini-pro"
        ]:
            try:
                g_model = genai.GenerativeModel(model_name=model_name)
                prompt = (
                    f"Explain the concept of '{topic}' in a simple, clear, and engaging way for a school student. "
                    f"Keep it under 3-4 concise paragraphs with an intuitive real-world analogy."
                )
                response = g_model.generate_content(prompt)
                if hasattr(response, "text") and response.text:
                    return response.text.strip()
            except Exception:
                continue

    # Fallback explanation if no API key is provided
    return (
        f"Explanation for '{topic}':\n\n"
        f"'{topic}' is an important subject! In simple terms, it refers to the core principles "
        f"and mechanisms that make this concept work in the real world.\n\n"
        f"💡 Tip: Configure your GEMINI_API_KEY in the .env file to enable live Gemini generative explanations."
    )

import os
import re
import json
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

def clean_json_block(text: str) -> str:
    """Removes Markdown ```json code fences and trims whitespace."""
    # Match markdown fence
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def _fallback_quiz(topic_or_text: str) -> list:
    """Provides fallback quiz questions for testing when API key is not yet configured."""
    t = topic_or_text.lower()
    if "pythagor" in t:
        return [
            {
                "question": "What does the Pythagorean theorem describe?",
                "options": [
                    "The relationship between the angles of a triangle.",
                    "The relationship between the sides of a right-angled triangle.",
                    "The relationship between the area and perimeter of a triangle.",
                    "The relationship between the sides of any triangle."
                ],
                "answer": "The relationship between the sides of a right-angled triangle."
            },
            {
                "question": "If 'a' and 'b' are the lengths of the two shorter sides of a right-angled triangle, and 'c' is the length of the longest side (hypotenuse), what equation represents the Pythagorean theorem?",
                "options": [
                    "a + b = c",
                    "a² + b² = c²",
                    "a² - b² = c²",
                    "2a + 2b = 2c"
                ],
                "answer": "a² + b² = c²"
            },
            {
                "question": "Which type of triangle does the Pythagorean theorem apply to?",
                "options": [
                    "Equilateral triangles",
                    "Isosceles triangles",
                    "Right-angled triangles",
                    "All types of triangles"
                ],
                "answer": "Right-angled triangles"
            }
        ]
    return [
        {
            "question": f"What is the primary significance of studying '{topic_or_text[:30]}'?",
            "options": [
                "It builds foundational knowledge in the subject domain.",
                "It is solely an abstract mathematical problem.",
                "It has no practical real-world applications.",
                "It was completely disproven in modern science."
            ],
            "answer": "It builds foundational knowledge in the subject domain."
        },
        {
            "question": "Which of the following best represents a core characteristic of this topic?",
            "options": [
                "Empirical evidence and systematic understanding",
                "Random unsupported assertions",
                "Subjective opinions without structure",
                "None of the above"
            ],
            "answer": "Empirical evidence and systematic understanding"
        },
        {
            "question": "How can learners best practice and master this concept?",
            "options": [
                "Passive observation only",
                "Hands-on exercises and conceptual problem-solving",
                "Skipping the basics directly to unrelated topics",
                "Memorizing without understanding"
            ],
            "answer": "Hands-on exercises and conceptual problem-solving"
        }
    ]

def generate_quiz(text: str) -> list:
    """
    Generates 3 multiple-choice questions from a passage or topic.
    Returns a Python list of question dictionaries.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        return _fallback_quiz(text)

    genai.configure(api_key=api_key)

    prompt = f"""You are a quiz generator.

From the following passage or topic, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON** ONLY, without markdown code fences or other prose:
[
  {{
    "question": "What is ...?",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "answer": "Option 1"
  }}
]

Passage / Topic:
{text}
"""

    last_error = None
    for model_name in CANDIDATE_MODELS:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt)
            if hasattr(response, "text") and response.text:
                quiz_text = response.text.strip()
                cleaned_text = clean_json_block(quiz_text)
                data = json.loads(cleaned_text)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except Exception as e:
            last_error = e
            continue

    print(f"Quiz generation with Gemini had error: {last_error}. Using fallback quiz.")
    return _fallback_quiz(text)

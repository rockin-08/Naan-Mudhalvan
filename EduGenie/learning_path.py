import os
import traceback
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

def _fallback_learning_path(topic: str) -> str:
    return f"""## {topic.upper()} Learning Path: From Zero to Hero

This learning path is structured to progressively introduce {topic} concepts, starting from the basics and gradually advancing to more complex topics. It's designed to be adaptive: feel free to adjust the pace and delve deeper into areas that particularly interest you.

### I. Beginner Level: Building a Foundation
**(Estimated Time: 1-2 weeks)**

* **Key Topics:**
  * Introduction to {topic} and fundamental principles
  * Basic Syntax, core terminology, and setup
  * Working with essential data types and primary operations
  * Simple guided practical exercises

* **Resources:**
  * **Interactive Tutorials:** FreeCodeCamp, W3Schools, Codecademy
  * **Video Tutorials:** YouTube crash courses and beginner playlists

---

### II. Intermediate Level: Core Application & Techniques
**(Estimated Time: 2-3 weeks)**

* **Key Topics:**
  * Real-world project implementation and structured workflows
  * Intermediate patterns, optimization, and debugging
  * Connecting with external libraries and tools
  * Mini-projects and hands-on scenarios

* **Resources:**
  * **Books / Documentation:** Official documentation and reference guides
  * **Practice Platforms:** GitHub sample repositories, LeetCode / HackerRank

---

### III. Advanced Level: Mastery & Production Readiness
**(Estimated Time: 3-4 weeks and beyond)**

* **Key Topics:**
  * Architectural design, scalability, and performance tuning
  * Advanced problem solving and best practices
  * Production deployment, testing, and continuous improvement

* **Resources:**
  * Specialized deep-dive courses (Coursera, Udemy, edX)
  * Community forums, technical papers, and developer blogs

---

**Adaptive Learning Tips:**
* Start with the basics: Don't rush into advanced topics before mastering the fundamentals.
* Practice regularly: Hands-on code and exercises solidify understanding.
* Break down complex problems into smaller, manageable parts.

💡 *Note: Set your GEMINI_API_KEY in .env to dynamically generate real-time AI learning recommendations tailored to any specific topic.*
"""

def get_learning_recommendations(topic: str) -> str:
    """Generates a personalized, structured learning path for any given topic using Gemini."""
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (books, tutorials, video courses).
Include:
- Level I: Beginner Level (with estimated timeline, key topics, resources)
- Level II: Intermediate Level (with estimated timeline, key topics, resources)
- Level III: Advanced Level (with estimated timeline, key topics, resources)
- Adaptive Learning Tips

Format in clean markdown with bullet points and bold headers.
"""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        return _fallback_learning_path(topic)

    genai.configure(api_key=api_key)

    last_error = None
    for model_name in CANDIDATE_MODELS:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            elif hasattr(response, "parts") and response.parts:
                return response.parts[0].text.strip()
        except Exception as e:
            last_error = e
            continue

    print(f"Gemini learning recommendations error: {last_error}")
    return _fallback_learning_path(topic)

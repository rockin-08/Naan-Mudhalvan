import os
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

load_dotenv()

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)

# Directories for static assets and HTML templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the EduGenie interactive dashboard."""
    has_api_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"has_api_key": has_api_key}
    )

# Q&A - GET API using Gemini
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}

# Explanation - POST API
@app.post("/explain")
async def explain_api(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}

# Summarization - POST API
@app.post("/summarize")
async def summarize_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}

# Quiz Generation - POST API
@app.post("/quiz")
async def quiz_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    print("Generated quiz:", quiz)  # DEBUG
    return JSONResponse(content={"quiz": quiz})

# Learning Recommendations - GET API
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}

# Optional endpoint to set API key from UI
@app.post("/api/set-key")
async def set_api_key(request: Request):
    data = await request.json()
    key = data.get("apiKey", "").strip()
    if key:
        os.environ["GEMINI_API_KEY"] = key
        # Persist to .env
        env_path = os.path.join(BASE_DIR, ".env")
        with open(env_path, "w") as f:
            f.write(f"GEMINI_API_KEY={key}\n")
        return {"status": "success", "message": "API key updated successfully!"}
    return JSONResponse(content={"error": "Invalid API key provided."}, status_code=400)

# Download Project Zip Endpoint
@app.get("/download")
async def download_zip():
    # Look for zip in parent directory or current directory
    zip_path = os.path.join(os.path.dirname(BASE_DIR), "EduGenie.zip")
    if not os.path.exists(zip_path):
        zip_path = os.path.join(BASE_DIR, "EduGenie.zip")
    if os.path.exists(zip_path):
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename="EduGenie.zip"
        )
    return JSONResponse(status_code=404, content={"error": "EduGenie.zip not found."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# 💡 EduGenie: Google Gemini Powered Learning Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4.svg?style=flat&logo=google&logoColor=white)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**EduGenie** is a lightweight AI-powered educational assistant that simplifies learning through generative AI. Designed for students and learners of all academic levels, EduGenie integrates cloud-based intelligence with an intuitive, responsive web interface.

---

## 🌟 Key Features

1. **Question & Answer (`/qa`)**:
   - Ask academic or general knowledge questions.
   - Receive smart, concise, and accurate answers powered by Google Gemini.

2. **Concept Explanation (`/explain`)**:
   - Simplifies complex topics into clear, school-level language with real-world analogies.
   - Powered by instruction-tuned AI models.

3. **Interactive Quiz Generation & Self-Assessment (`/quiz`)**:
   - Automatically generates 3 multiple-choice questions (MCQs) with 4 options per topic/passage.
   - Instant real-time answer verification with visual feedback (`✅ Correct!` / `❌ Incorrect`).

4. **Passage Summarization (`/summarize`)**:
   - Condenses lengthy textbook excerpts and articles into clear revision summaries without losing essential context.

5. **Structured Learning Roadmaps (`/learn/recommendations`)**:
   - Generates customized study roadmaps from Beginner to Advanced levels.
   - Includes estimated timelines, recommended books, documentation, and video courses.

---

## 🏗️ Architecture & Tech Stack

- **Backend**: FastAPI (Python ASGI framework)
- **AI Models**:
  - Google Gemini 1.5 Pro / Flash (via Gemini API)
  - LaMini-Flan-T5-783M (Local HuggingFace model support)
- **Frontend**: Responsive HTML5, CSS3, JavaScript (Fetch API)
- **Templating**: Jinja2
- **Server**: Uvicorn ASGI Server

---

## 📁 Repository Structure

```text
EduGenie/
├── main.py                 # FastAPI application & REST API routes
├── qna.py                  # Question answering module (Gemini)
├── explanation_module.py   # Concept explanation module (LaMini / Gemini)
├── quiz_module.py          # Quiz generation & JSON parsing module
├── summary_module.py       # Passage summarization module
├── learning_path.py        # Structured learning recommendations module
├── templates/
│   └── index.html          # Interactive web UI dashboard
├── static/
│   └── style.css           # Modern responsive styles
├── requirements.txt        # Python dependencies
├── run.bat                 # One-click Windows startup script
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone or Extract the Project
```bash
git clone https://github.com/<your-username>/EduGenie.git
cd EduGenie
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
> *You can obtain a free Gemini API key from [Google AI Studio](https://aistudio.google.com/). You can also configure the key directly in the web UI navigation bar.*

### 5. Run the Application
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Or simply double-click **`run.bat`** on Windows.

### 6. Open in Browser
Visit: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🔌 API Endpoints Reference

| Endpoint | Method | Parameter / Payload | Description |
|---|---|---|---|
| `/` | `GET` | None | Renders the EduGenie Web Dashboard |
| `/qa` | `GET` | `?question=<string>` | Returns answer to an academic question |
| `/explain` | `POST` | `{"topic": "<string>"}` | Returns student-friendly concept explanation |
| `/summarize` | `POST` | `{"text": "<string>"}` | Returns condensed text summary |
| `/quiz` | `POST` | `{"text": "<string>"}` | Returns 3 MCQs in structured JSON format |
| `/learn/recommendations` | `GET` | `?topic=<string>` | Returns 3-tier structured learning path |
| `/api/set-key` | `POST` | `{"apiKey": "<string>"}` | Configures Gemini API key dynamically |

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

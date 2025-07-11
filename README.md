# 🏋️‍♂️ GymGuru - AI-Powered Gym Registration Chatbot

Welcome to **GymGuru**, an AI-powered gym registration system designed to provide an intelligent and interactive experience for users who want to register at the gym, get fitness advice, and manage their membership efficiently.

> 🚀 Powered by **Google Gemini 2.5 API** and built with **FastAPI**, **SQLAlchemy**, and **WebSockets**.

---

## 📌 Features

- ✅ AI-assisted Gym Registration using Google Gemini
- 💬 Real-time WebSocket-based chat interface
- 📚 Persistent chat history using PostgreSQL
- 🔒 Smart conversation flow with one-question-at-a-time logic
- 📊 Dynamic membership and fitness goal references
- 📂 Tool function support for user registration via Gemini API
- 🧠 Context-aware chatbot trained for fitness-specific queries

---

## 🛠️ Tech Stack

| Technology     | Purpose                        |
|----------------|---------------------------------|
| FastAPI        | Backend Web Framework           |
| SQLAlchemy     | ORM for Database Interaction    |
| Google Gemini  | AI Chatbot API (Text & Tools)   |
| WebSockets     | Real-time Bi-directional Chat   |
| Jinja2         | HTML Templating (Frontend)      |
| PostgreSql | Database                        |

---

## 🧠 AI Model Behavior

The chatbot is trained to collect:
- `full_name`
- `gender` (male/female/other)
- `date_of_birth`
- `email` (optional)
- `phone_number` (optional)
- `address` (optional)
- `fitness_goal` (weight_loss/muscle_building/general_fitness/sports_training)
- `membership` (basic/premium)

The AI:
- Asks one question at a time with explanation
- Follows strict rule-based prompts
- Accepts only gym-related queries
- Automatically registers users using tool functions when all data is collected

---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git https://github.com/anshulthakur01/GymGuru.git
```

### 2. Create `.env`

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run FastAPI App

```bash
uvicorn main:app --reload
```

### 5. Visit the App

Open your browser at: [http://localhost:8000](http://localhost:8000)

---

## 📂 Project Structure

```
GymGuru/
├── db/
│   ├── database.py
│   └── models.py
├── static/
│   └── ...
├── templates/
│   └── index.html
├── utils/
│   ├── chat_service.py
│   ├── enums.py
│   ├── helpers.py
│   └── tools_conf.py
├── main.py
├── config.py
├── README.md
└── requirements.txt
```

---

## 📡 WebSocket API

- **Endpoint:** `/ws`
- **Message Format:**

```json
{
  "message": "Hi, I want to join the gym"
}
```

- **AI Response:**

Returns a structured JSON with the bot's next question or confirmation message.

---

## 🧪 Example JSON Response

```json
{
  "all_required_answered": false,
  "answered_count": 3,
  "total_questions": 8,
  "data": {
    "full_name": "John Doe",
    "gender": "male",
    "date_of_birth": "1990-01-01"
  },
  "ai_message": "Please provide your email to proceed. We use this to send you updates and offers."
}
```

---

## 🙌 Acknowledgments

- [Google Gemini API](https://cloud.google.com/vertex-ai/docs/generative-ai/overview)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
---
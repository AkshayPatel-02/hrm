# 🤖 HRM Candidate Screening Chatbot

An interactive AI-powered chatbot that screens candidates using a rule-based Hierarchical Reasoning Model (HRM) with natural language input.

## ✨ Features

- 💬 **Conversational Interface** - Describe jobs and candidates in plain English
- 📊 **Clean Results Table** - No raw JSON, just readable decisions
- 🔍 **Explainable Decisions** - Every decision backed by transparent HRM rules
- 🎯 **9-Layer Rule System** - Deterministic screening (R1-R9)
- 🤝 **LLM + HRM** - Best of both: AI parsing + rule-based decisions

## 🚀 Quick Start

### 1. Start Backend

```bash
cd backend
pip install -r requirements.txt

# Add your Gemini API key to .env
echo "GEMINI_API_KEY=your_key_here" > .env

# Start server with auto-reload
uvicorn main:app --reload --port 8000
```

### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Use the Chatbot

Open http://localhost:5173 and:

1. **Describe the job**: "I need a Backend Engineer with 3+ years Python experience, FastAPI knowledge, and a Bachelor's degree"

2. **Describe candidates**: "Alice has 5 years Python and FastAPI with a CS degree. Bob has 2 years Python only."

3. **View results** in a clean table with decisions and explanations!

## 🎯 How It Works

```
User Input (Natural Language)
    ↓
Gemini LLM (Parse & Structure)
    ↓
HRM Engine (Apply 9 Rules)
    ↓
Gemini LLM (Format Explanations)
    ↓
Clean Results Table
```

### HRM Rules (R1-R9)

**Layer 1 - Eligibility Gate:**
- R1: Minimum experience check
- R2: Mandatory skills validation
- R3: Education requirement

**Layer 2 - Risk Evaluation:**
- R4: Skill gap assessment
- R5: Employment gaps check
- R6: Certification requirements

**Layer 3 - Policy Decision:**
- R7: HIRE policy
- R8: REVIEW policy
- R9: REJECT policy

## 📁 Project Structure

```
HRM/
├── backend/
│   ├── main.py              # FastAPI app with chat endpoints
│   ├── chat_handler.py      # Conversation manager
│   ├── hrm_engine.py        # 3-layer rule engine
│   ├── llm_service.py       # Gemini API integration
│   └── models.py            # Data schemas
├── frontend/
│   └── src/
│       └── screens/
│           └── ChatInterface.jsx  # Main chatbot UI
└── README.md
```

## 🎨 UI Preview

The chatbot shows:
- **Chat messages** (user vs system)
- **Results table** with color-coded decisions
- **Detailed breakdowns** with expandable HRM traces
- **Start new** button to reset and screen more candidates

## 🔧 API Endpoints

### `GET /api/chat/start`
Start a new conversation session

### `POST /api/chat/message`
```json
{
  "session_id": "uuid",
  "message": "User's natural language input"
}
```

Returns formatted response with results when screening is complete.

## 🎯 Example Conversation

**System:**
> 👋 Welcome! Please describe the job role you're hiring for.

**You:**
> Senior Python Developer, 3 years FastAPI, Bachelor's required

**System:**
> ✅ Got it! Position: Senior Python Developer
> Required: Python, FastAPI
> Min Experience: 3 years
> 
> Now describe your candidates.

**You:**
> Alice: 5 years Python+FastAPI, Bachelor's
> Bob: 2 years Python only

**System:**
> 📊 Screening Complete!
> 
> | Name  | Decision | Reasoning |
> |-------|----------|-----------|
> | Alice | HIRE     | Strong match: exceeds requirements... |
> | Bob   | REJECT   | Below minimum experience (R1)... |

## 🔐 Environment Variables

Create `backend/.env`:
```
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-flash
```

Get your API key from: https://makersuite.google.com/app/apikey

## 🎯 Key Differentiators

| Aspect | LLM-Only | LLM + HRM |
|--------|----------|-----------|
| Consistency | ❌ Variable | ✅ Deterministic |
| Explainability | ❌ Opaque | ✅ Full trace |
| Auditability | ❌ None | ✅ Complete |
| User Experience | ❌ Technical | ✅ Friendly |

## 🐛 Troubleshooting

**CORS errors?**
- Make sure backend is running on port 8000
- Frontend on port 5173
- Both servers must be running

**No API key?**
- Set `GEMINI_API_KEY` in `backend/.env`
- Restart backend after adding key

**Slow responses?**
- LLM processing takes 15-20 seconds for 5 candidates
- This is normal - you'll see a typing indicator

## 📝 License

Hackathon demo project - 2026

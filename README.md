# HRM Candidate Screening System

> **Explainable AI for Hiring**: Demonstrating why LLM-only screening is unreliable and how rule-based HRM ensures consistent, traceable decisions.

## 🎯 Problem Statement

Organizations increasingly rely on AI for candidate screening, but LLM-based decisions are **inconsistent**, **opaque**, and hard to justify, making them unreliable for high-impact hiring decisions.

## 💡 What This MVP Demonstrates

This is a **trust demo**, not an accuracy demo. It shows:

1. ❌ **Why LLM-only screening is unreliable** - Same input may produce different outputs
2. ✅ **How rule-based HRM enforces consistency** - Deterministic decisions every time  
3. 📋 **How every decision can be traced and explained** - Full reasoning traces with named rules
4. ⚖️ **How decisions can be defended** - Compliance with hiring policies

## 🏗️ System Architecture

```
Web UI (React + Vite)
   ↓
FastAPI Backend
   ↓
Gemini LLM (parsing only)
   ↓
HRM Engine (3-layer decision system)
   ↓
Decision + Reasoning Trace
```

### HRM 3-Layer Architecture

**Layer 1: Eligibility Gate** (Hard Filters)
- R1_MIN_EXPERIENCE - Minimum years required
- R2_MANDATORY_SKILLS - Required skills check
- R3_EDUCATION_REQUIREMENT - Education level validation

**Layer 2: Risk & Gap Evaluation**
- R4_SKILL_GAP_THRESHOLD - Preferred skills coverage
- R5_EMPLOYMENT_GAP - Gap analysis with explanations
- R6_CERTIFICATION_MISSING - Certification requirements

**Layer 3: Policy Decision**
- R7_HIRE_POLICY - Low risk → Hire
- R8_REVIEW_POLICY - Medium risk → Review
- R9_REJECT_POLICY - High risk → Reject

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run server
python main.py
```

Backend will run at: http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run at: http://localhost:5173

## 📊 Usage

1. **Upload Data**: Navigate to http://localhost:5173
   - Click "Load Demo Data" for quick testing
   - Or manually enter job role and candidates in JSON format

2. **View Results**: See all candidates with both decisions
   - Green badge = HIRE
   - Yellow badge = REVIEW
   - Red badge = REJECT

3. **Compare Decisions**: Click any candidate to see:
   - **Left Panel**: LLM-only decision (opaque, opinionated)
   - **Right Panel**: HRM decision (structured, rule-based)
   - Expand reasoning steps to see which rules triggered

## 🎬 Demo Flow (< 2 minutes)

1. Click "Load Demo Data" → "Screen Candidates"
2. Observe 5 candidates with varying qualifications
3. Click on a candidate where decisions differ
4. Show the expandable reasoning trace
5. Highlight how HRM is:
   - ✅ Deterministic
   - ✅ Explainable  
   - ✅ Traceable
   - ✅ Compliant

## 🔍 Sample Data

The demo includes 5 candidates:

- **Alice Johnson**: Strong candidate (hire)
- **Bob Smith**: Borderline with explained gap (review)
- **Carol Martinez**: Below experience threshold (reject)
- **David Lee**: Strong but unexplained gap (flagged)
- **Eva Rodriguez**: Wrong skill set (reject)

## 🛡️ Key Differentiators

| Feature | LLM-Only | LLM + HRM |
|---------|----------|-----------|
| Consistency | ❌ Variable | ✅ Deterministic |
| Explainability | ❌ Opaque | ✅ Full trace |
| Traceability | ❌ None | ✅ Named rules |
| Compliance | ❌ Uncertain | ✅ Policy-enforced |
| Auditability | ❌ Impossible | ✅ Complete |

## 📁 Project Structure

```
HRM/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Data models
│   ├── hrm_engine.py        # 3-layer HRM logic
│   ├── llm_service.py       # Gemini integration
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── screens/
│   │   │   ├── UploadScreen.jsx
│   │   │   ├── CandidateListScreen.jsx
│   │   │   └── ComparisonScreen.jsx
│   │   ├── components/
│   │   │   └── Header.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
└── README.md
```

## 🎓 Technical Highlights

- **Backend**: FastAPI with Pydantic validation
- **LLM**: Google Gemini for structured extraction only
- **HRM**: Pure Python rule engine (no ML)
- **Frontend**: React 18 + Vite for fast development
- **Design**: Clean, minimal, comparison-focused UI

## 🚫 Out of Scope

This MVP explicitly does NOT:
- ❌ Predict the best candidate
- ❌ Train ML models
- ❌ Make bias predictions
- ❌ Automate real hiring decisions
- ❌ Optimize for accuracy metrics

## 📝 License

This is a hackathon demo project.

## 🙏 Acknowledgments

Built for demonstrating explainable AI in hiring decisions.

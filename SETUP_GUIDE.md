# SETUP GUIDE - Start Here!

## 🚀 Quick Setup

### Step 1: Backend Setup

1. Open a terminal in the `backend` folder:
   ```bash
   cd backend
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. **IMPORTANT**: Configure your Gemini API Key:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Get a Gemini API key from: https://makersuite.google.com/app/apikey
   - Open `.env` and replace `your_api_key_here` with your actual API key

6. Run the backend server:
   ```bash
   python main.py
   ```
   
   ✅ Backend should be running at: http://localhost:8000

### Step 2: Frontend Setup

1. Open a NEW terminal in the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   
   ✅ Frontend should be running at: http://localhost:5173

### Step 3: Test the Application

1. Open your browser to: http://localhost:5173

2. Click **"Load Demo Data"** button

3. Click **"Screen Candidates"**

4. View the results and click on any candidate to see the comparison!

## 🎬 Demo Script for Judges

### 1-Minute Demo Flow:

1. **Start**: "This system demonstrates why LLM-only screening is unreliable"

2. **Upload**: Click "Load Demo Data" → "Screen Candidates" (5 seconds)

3. **Results**: "Notice how some candidates have different decisions between LLM and HRM" (10 seconds)

4. **Comparison**: Click on David Lee
   - **Left Panel**: "LLM gives an opinion but no traceability"
   - **Right Panel**: "HRM shows exactly which rules triggered and why"
   - Expand reasoning steps to show R5_EMPLOYMENT_GAP flagged

5. **Key Point**: "Same input to HRM always gives same output. LLM? Not guaranteed."

6. **Conclusion**: "This makes hiring decisions explainable, compliant, and defensible."

## 🔑 Key Features to Highlight

1. **Deterministic**: Run the same candidate multiple times → same result with HRM
2. **Traceable**: Every decision has a complete reasoning trace
3. **Named Rules**: R1-R9 are policy-enforced, not opinions
4. **Layered**: 3-layer architecture (Eligibility → Risk → Policy)
5. **Explainable**: Can justify every decision to stakeholders

## 🐛 Troubleshooting

**Backend won't start:**
- Make sure you've activated the virtual environment
- Check if you've set the GEMINI_API_KEY in `.env`
- Verify Python version: `python --version` (should be 3.8+)

**Frontend won't start:**
- Check Node version: `node --version` (should be 16+)
- Delete `node_modules` and run `npm install` again

**API errors:**
- Verify backend is running at http://localhost:8000
- Check browser console for CORS errors
- Ensure Gemini API key is valid

## 📊 Sample Data Explained

The demo includes 5 diverse candidates:

| Candidate | Expected Result | Why |
|-----------|----------------|-----|
| Alice Johnson | HIRE | Perfect match, all skills, certifications |
| Bob Smith | REVIEW | Good but small explained gap |
| Carol Martinez | REJECT | Below minimum experience (R1) |
| David Lee | REVIEW | Strong but 8-month unexplained gap (R5) |
| Eva Rodriguez | REJECT | Missing all required skills (R2) |

## 🎯 Judge Questions & Answers

**Q: Why not just use LLM?**
A: LLMs are inconsistent. Same input may give different outputs. For high-stakes decisions like hiring, you need deterministic, auditable results.

**Q: Can't LLMs explain their reasoning?**
A: LLM explanations are post-hoc rationalizations. HRM traces show the ACTUAL rules that fired.

**Q: Is this production-ready?**
A: This is a proof-of-concept. The HRM engine demonstrates the principle. Production systems would integrate with existing HR systems.

**Q: What about bias?**
A: HRM rules are transparent and auditable. If a rule is biased, you can identify and fix it. LLM bias is opaque.

## 🚀 Next Steps (Post-Hackathon)

If continuing this project:

1. Add more sophisticated rules
2. Integrate with ATS (Applicant Tracking Systems)
3. Add rule configuration UI for HR teams
4. Implement A/B testing framework
5. Add compliance reports generation

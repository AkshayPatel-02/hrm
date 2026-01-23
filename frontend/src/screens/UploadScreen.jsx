import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

function UploadScreen({ setScreeningResults, setJobRole }) {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Form state
  const [jobRoleText, setJobRoleText] = useState('')
  const [candidatesJson, setCandidatesJson] = useState('')
  const [useDemo, setUseDemo] = useState(false)

  const demoJobRole = {
    "job_id": "job_001",
    "title": "Senior Python Developer",
    "required_skills": ["Python", "FastAPI", "REST API"],
    "preferred_skills": ["Docker", "PostgreSQL", "AWS"],
    "min_experience": 3,
    "education_required": "bachelors"
  }

  const demoCandidates = [
    {
      "candidate_id": "cand_001",
      "name": "Alice Johnson",
      "skills": ["Python", "FastAPI", "REST API", "Docker", "PostgreSQL"],
      "experience_years": 5,
      "education_level": "bachelors",
      "certifications": ["AWS Certified Developer"],
      "employment_gaps": []
    },
    {
      "candidate_id": "cand_002",
      "name": "Bob Smith",
      "skills": ["Python", "Django", "REST API"],
      "experience_years": 3.5,
      "education_level": "bachelors",
      "certifications": [],
      "employment_gaps": [
        { "months": 4, "reason_provided": true }
      ]
    },
    {
      "candidate_id": "cand_003",
      "name": "Carol Martinez",
      "skills": ["Python", "FastAPI"],
      "experience_years": 2,
      "education_level": "bachelors",
      "certifications": [],
      "employment_gaps": []
    },
    {
      "candidate_id": "cand_004",
      "name": "David Lee",
      "skills": ["Python", "FastAPI", "REST API", "AWS"],
      "experience_years": 4,
      "education_level": "masters",
      "certifications": ["AWS Certified Solutions Architect"],
      "employment_gaps": [
        { "months": 8, "reason_provided": false }
      ]
    },
    {
      "candidate_id": "cand_005",
      "name": "Eva Rodriguez",
      "skills": ["JavaScript", "Node.js", "React"],
      "experience_years": 6,
      "education_level": "bachelors",
      "certifications": [],
      "employment_gaps": []
    }
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      let jobRole, candidates

      if (useDemo) {
        jobRole = demoJobRole
        candidates = demoCandidates
      } else {
        // Parse JSON inputs
        try {
          jobRole = JSON.parse(jobRoleText || '{}')
          candidates = JSON.parse(candidatesJson || '[]')
        } catch (err) {
          throw new Error('Invalid JSON format. Please check your input.')
        }
      }

      // Send to backend
      const response = await axios.post(`${API_BASE}/api/screen`, {
        job_role: jobRole,
        candidates: candidates
      })

      // Store results and navigate
      setJobRole(jobRole)
      setScreeningResults(response.data)
      navigate('/candidates')

    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const loadDemo = () => {
    setJobRoleText(JSON.stringify(demoJobRole, null, 2))
    setCandidatesJson(JSON.stringify(demoCandidates, null, 2))
    setUseDemo(false)
  }

  return (
    <div className="container">
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h1 className="text-center">Upload Job & Candidates</h1>
        <p className="text-center mb-4">
          Compare LLM-only vs. HRM-based candidate screening
        </p>

        {error && (
          <div style={{ 
            background: '#fee2e2', 
            color: '#991b1b', 
            padding: '1rem', 
            borderRadius: '8px',
            marginBottom: '1.5rem'
          }}>
            {error}
          </div>
        )}

        <div className="card">
          <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
            <button 
              type="button"
              onClick={loadDemo}
              className="btn"
              style={{ 
                background: 'var(--bg-secondary)',
                color: 'var(--primary-color)',
                border: '2px solid var(--primary-color)'
              }}
            >
              Load Demo Data
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Job Role (JSON)</label>
              <textarea
                className="textarea"
                value={jobRoleText}
                onChange={(e) => setJobRoleText(e.target.value)}
                placeholder={JSON.stringify(demoJobRole, null, 2)}
                style={{ fontFamily: 'monospace', fontSize: '0.875rem' }}
                rows={8}
              />
              <small style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                Required fields: job_id, title, required_skills, min_experience, education_required
              </small>
            </div>

            <div className="form-group">
              <label className="form-label">Candidates (JSON Array)</label>
              <textarea
                className="textarea"
                value={candidatesJson}
                onChange={(e) => setCandidatesJson(e.target.value)}
                placeholder={JSON.stringify([demoCandidates[0]], null, 2)}
                style={{ fontFamily: 'monospace', fontSize: '0.875rem' }}
                rows={12}
              />
              <small style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                Required fields per candidate: candidate_id, name, skills, experience_years, education_level
              </small>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary" 
              disabled={loading}
              style={{ width: '100%' }}
            >
              {loading ? 'Processing...' : 'Screen Candidates'}
            </button>
          </form>
        </div>

        <div className="card mt-3" style={{ background: 'var(--bg-secondary)' }}>
          <h3>Quick Demo Mode</h3>
          <p style={{ fontSize: '0.875rem' }}>
            Click "Load Demo Data" to populate both fields with sample data, or check the box below to use demo data directly.
          </p>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
            <input 
              type="checkbox"
              checked={useDemo}
              onChange={(e) => setUseDemo(e.target.checked)}
            />
            <span>Use demo data (ignore text fields above)</span>
          </label>
        </div>
      </div>
    </div>
  )
}

export default UploadScreen

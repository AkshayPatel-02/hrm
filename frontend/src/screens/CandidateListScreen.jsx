import { useNavigate } from 'react-router-dom'
import { useEffect } from 'react'

function CandidateListScreen({ results, jobRole }) {
  const navigate = useNavigate()

  useEffect(() => {
    if (!results) {
      navigate('/')
    }
  }, [results, navigate])

  if (!results) {
    return null
  }

  const handleCandidateClick = (candidateId) => {
    navigate(`/compare/${candidateId}`)
  }

  return (
    <div className="container">
      <h1>Screening Results</h1>
      <p style={{ marginBottom: '2rem' }}>
        Click on any candidate to see detailed comparison between LLM-only and HRM decisions
      </p>

      {jobRole && (
        <div className="card mb-4" style={{ background: 'var(--bg-secondary)' }}>
          <h3>Job Role: {jobRole.title}</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
            <div>
              <strong>Required Skills:</strong>
              <div style={{ marginTop: '0.5rem' }}>
                {jobRole.required_skills.map(skill => (
                  <span key={skill} style={{
                    display: 'inline-block',
                    background: '#dbeafe',
                    color: '#1e40af',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    marginRight: '0.5rem',
                    marginBottom: '0.5rem',
                    fontSize: '0.875rem'
                  }}>
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <strong>Minimum Experience:</strong> {jobRole.min_experience} years<br />
              <strong>Education:</strong> {jobRole.education_required}
            </div>
          </div>
        </div>
      )}

      <div className="grid">
        {results.results.map((result) => (
          <div 
            key={result.candidate_id}
            className="candidate-card"
            onClick={() => handleCandidateClick(result.candidate_id)}
          >
            <div className="candidate-header">
              <div>
                <h3 className="candidate-name">{result.candidate_name}</h3>
                <div className="candidate-id">ID: {result.candidate_id}</div>
              </div>
            </div>

            <div className="decision-badges">
              <div className="decision-group">
                <div className="decision-label">LLM Only</div>
                <span className={`badge badge-${result.llm_only.decision.toLowerCase()}`}>
                  {result.llm_only.decision}
                </span>
              </div>

              <div className="decision-group">
                <div className="decision-label">LLM + HRM</div>
                <span className={`badge badge-${result.hrm_decision.decision.toLowerCase()}`}>
                  {result.hrm_decision.decision}
                </span>
              </div>
            </div>

            {result.llm_only.decision !== result.hrm_decision.decision && (
              <div style={{
                marginTop: '1rem',
                padding: '0.75rem',
                background: '#fef3c7',
                borderRadius: '6px',
                fontSize: '0.875rem',
                fontWeight: 500,
                color: '#92400e'
              }}>
                ⚠️ Decisions differ - click to see why
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default CandidateListScreen

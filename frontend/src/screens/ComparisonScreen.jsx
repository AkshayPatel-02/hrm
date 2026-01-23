import { useParams, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'

function ComparisonScreen({ results }) {
  const { candidateId } = useParams()
  const navigate = useNavigate()
  const [expandedSteps, setExpandedSteps] = useState({})

  useEffect(() => {
    if (!results) {
      navigate('/')
    }
  }, [results, navigate])

  if (!results) {
    return null
  }

  const candidate = results.results.find(r => r.candidate_id === candidateId)

  if (!candidate) {
    return (
      <div className="container">
        <div className="card">
          <h2>Candidate not found</h2>
          <button onClick={() => navigate('/candidates')} className="btn btn-primary mt-3">
            Back to Candidates
          </button>
        </div>
      </div>
    )
  }

  const toggleStep = (index) => {
    setExpandedSteps(prev => ({
      ...prev,
      [index]: !prev[index]
    }))
  }

  return (
    <div className="container">
      <div style={{ marginBottom: '2rem' }}>
        <h1>{candidate.candidate_name}</h1>
        <p style={{ fontSize: '0.875rem' }}>ID: {candidate.candidate_id}</p>
      </div>

      <div className="split-view">
        {/* LLM Only Panel */}
        <div className="panel">
          <div className="panel-header">
            <h2 className="panel-title" style={{ color: '#9333ea' }}>
              🤖 LLM Only
            </h2>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
              Opinionated • Inconsistent • Opaque
            </p>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ marginBottom: '1rem' }}>
              <span className="decision-label">Decision</span><br />
              <span className={`badge badge-${candidate.llm_only.decision.toLowerCase()}`} style={{ fontSize: '1rem', padding: '0.5rem 1rem', marginTop: '0.5rem' }}>
                {candidate.llm_only.decision}
              </span>
            </div>

            <div style={{ 
              background: 'var(--bg-secondary)',
              padding: '1rem',
              borderRadius: '8px',
              borderLeft: '4px solid #9333ea'
            }}>
              <strong style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                Explanation:
              </strong>
              <p style={{ marginTop: '0.5rem', marginBottom: 0, fontSize: '0.95rem' }}>
                {candidate.llm_only.explanation}
              </p>
            </div>
          </div>

          <div style={{
            background: '#fef3c7',
            padding: '1rem',
            borderRadius: '8px',
            fontSize: '0.875rem',
            color: '#92400e'
          }}>
            <strong>⚠️ Issues with LLM-only approach:</strong>
            <ul style={{ marginTop: '0.5rem', marginBottom: 0, paddingLeft: '1.5rem' }}>
              <li>No traceability of decision logic</li>
              <li>Same input may produce different results</li>
              <li>Cannot explain WHY this decision was made</li>
              <li>No rule enforcement or compliance</li>
            </ul>
          </div>
        </div>

        {/* HRM Panel */}
        <div className="panel" style={{ borderColor: 'var(--primary-color)', borderWidth: '3px' }}>
          <div className="panel-header">
            <h2 className="panel-title" style={{ color: 'var(--primary-color)' }}>
              ⚖️ LLM + HRM
            </h2>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
              Rule-based • Consistent • Explainable
            </p>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ marginBottom: '1rem' }}>
              <span className="decision-label">Decision</span><br />
              <span className={`badge badge-${candidate.hrm_decision.decision.toLowerCase()}`} style={{ fontSize: '1rem', padding: '0.5rem 1rem', marginTop: '0.5rem' }}>
                {candidate.hrm_decision.decision}
              </span>
            </div>
          </div>

          <div>
            <h3 style={{ fontSize: '1rem', marginBottom: '1rem', color: 'var(--primary-color)' }}>
              📋 Reasoning Trace
            </h3>
            
            <div className="reasoning-trace">
              {candidate.hrm_decision.reasoning_trace.map((step, index) => (
                <div 
                  key={index}
                  className={`reasoning-step ${step.result.toLowerCase()}`}
                >
                  <div className="step-header">
                    <span className="step-layer">{step.layer}</span>
                    <span className="step-rule">{step.rule}</span>
                  </div>
                  
                  <div className="step-result">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <span style={{ 
                          fontWeight: 600,
                          color: step.result === 'PASS' ? 'var(--success-color)' :
                                 step.result === 'FAIL' ? 'var(--danger-color)' :
                                 step.result === 'FLAGGED' ? 'var(--warning-color)' :
                                 'var(--primary-color)'
                        }}>
                          {step.result}
                        </span>
                      </div>
                      <button
                        onClick={() => toggleStep(index)}
                        style={{
                          background: 'none',
                          border: 'none',
                          cursor: 'pointer',
                          fontSize: '0.875rem',
                          color: 'var(--primary-color)',
                          fontWeight: 500
                        }}
                      >
                        {expandedSteps[index] ? '▼ Hide' : '▶ Details'}
                      </button>
                    </div>
                    
                    {expandedSteps[index] && (
                      <div className="step-explanation" style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid var(--border-color)' }}>
                        {step.explanation}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div style={{
            background: '#d1fae5',
            padding: '1rem',
            borderRadius: '8px',
            fontSize: '0.875rem',
            color: '#065f46',
            marginTop: '1.5rem'
          }}>
            <strong>✅ Benefits of HRM approach:</strong>
            <ul style={{ marginTop: '0.5rem', marginBottom: 0, paddingLeft: '1.5rem' }}>
              <li>Every decision is fully traceable</li>
              <li>Deterministic: same input = same output</li>
              <li>Each rule is named and explainable</li>
              <li>Compliant with hiring policies</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ComparisonScreen

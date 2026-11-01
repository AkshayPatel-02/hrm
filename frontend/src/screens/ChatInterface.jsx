import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

function ChatInterface() {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [sessionId, setSessionId] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [results, setResults] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  useEffect(() => {
    // Start chat session on mount
    startChat()
  }, [])

  const startChat = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/chat/start`)
      setSessionId(response.data.session_id)
      setMessages([{
        role: 'assistant',
        content: response.data.message
      }])
    } catch (error) {
      console.error('Error starting chat:', error)
      setMessages([{
        role: 'assistant',
        content: '❌ Failed to connect to the server. Please make sure the backend is running.'
      }])
    }
  }

  const sendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage = {
      role: 'user',
      content: inputMessage
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)

    try {
      const response = await axios.post(`${API_BASE}/api/chat/message`, {
        session_id: sessionId,
        message: inputMessage
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      setIsTyping(false)

      // Add assistant's response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.message
      }])

      // If results are ready, show them
      if (response.data.results) {
        setResults(response.data.results)
      }

      // Update session ID if changed
      if (response.data.session_id) {
        setSessionId(response.data.session_id)
      }

    } catch (error) {
      setIsTyping(false)
      console.error('Error sending message:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '❌ Sorry, there was an error processing your message. Please try again.'
      }])
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const startNewScreening = () => {
    setResults(null)
    setMessages([])
    startChat()
  }

  const getDecisionColor = (decision) => {
    switch (decision.toUpperCase()) {
      case 'HIRE': return '#10b981'
      case 'REVIEW': return '#f59e0b'
      case 'REJECT': return '#ef4444'
      default: return '#6b7280'
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>🤖 HRM Candidate Screening Assistant</h1>
        <p>Powered by AI + Rule-Based HRM</p>
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content.split('\n').map((line, i) => (
                <p key={i}>{line}</p>
              ))}
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="message assistant">
            <div className="message-content typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        {results && (
          <div className="results-section">
            <h2>📊 Screening Results</h2>
            
            <div className="results-table-container">
              <table className="results-table">
                <thead>
                  <tr>
                    <th>Candidate Name</th>
                    <th>Decision</th>
                    <th>Key Reasons</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((result, idx) => (
                    <tr key={idx}>
                      <td className="candidate-name">{result.name}</td>
                      <td>
                        <span 
                          className="decision-badge"
                          style={{ backgroundColor: getDecisionColor(result.decision) }}
                        >
                          {result.decision}
                        </span>
                      </td>
                      <td className="explanation">{result.explanation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="detailed-explanations">
              <h3>💡 Detailed Decision Breakdown</h3>
              {results.map((result, idx) => (
                <div key={idx} className="candidate-breakdown">
                  <h4 style={{ color: getDecisionColor(result.decision) }}>
                    {result.name} - {result.decision}
                  </h4>
                  <p className="summary-explanation">{result.explanation}</p>
                  
                  <details>
                    <summary>View Full HRM Reasoning Trace</summary>
                    <div className="reasoning-trace-detail">
                      {result.reasoning_trace.map((step, stepIdx) => (
                        <div key={stepIdx} className={`trace-step ${step.result.toLowerCase()}`}>
                          <div className="trace-header">
                            <span className="trace-layer">{step.layer}</span>
                            <span className="trace-rule">{step.rule}</span>
                            <span className={`trace-result ${step.result.toLowerCase()}`}>
                              {step.result}
                            </span>
                          </div>
                          <p className="trace-explanation">{step.explanation}</p>
                        </div>
                      ))}
                    </div>
                  </details>
                </div>
              ))}
            </div>

            <button 
              className="btn btn-primary"
              onClick={startNewScreening}
              style={{ marginTop: '2rem', width: '100%' }}
            >
              🔄 Start New Screening
            </button>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {!results && (
        <div className="chat-input-container">
          <input
            type="text"
            className="chat-input"
            placeholder="Type your message..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isTyping}
          />
          <button 
            className="send-button"
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isTyping}
          >
            ⬆️
          </button>
        </div>
      )}
    </div>
  )
}

export default ChatInterface

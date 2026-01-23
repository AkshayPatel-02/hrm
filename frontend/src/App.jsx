import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import Header from './components/Header'
import UploadScreen from './screens/UploadScreen'
import CandidateListScreen from './screens/CandidateListScreen'
import ComparisonScreen from './screens/ComparisonScreen'

function App() {
  const [screeningResults, setScreeningResults] = useState(null)
  const [jobRole, setJobRole] = useState(null)

  return (
    <Router>
      <div className="app">
        <Header />
        <Routes>
          <Route 
            path="/" 
            element={
              <UploadScreen 
                setScreeningResults={setScreeningResults}
                setJobRole={setJobRole}
              />
            } 
          />
          <Route 
            path="/candidates" 
            element={
              <CandidateListScreen 
                results={screeningResults}
                jobRole={jobRole}
              />
            } 
          />
          <Route 
            path="/compare/:candidateId" 
            element={
              <ComparisonScreen 
                results={screeningResults}
              />
            } 
          />
        </Routes>
      </div>
    </Router>
  )
}

export default App

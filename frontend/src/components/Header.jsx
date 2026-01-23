import { Link, useLocation } from 'react-router-dom'

function Header() {
  const location = useLocation()

  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="logo">
          HRM Candidate Screening
        </Link>
        <nav>
          {location.pathname === '/candidates' && (
            <Link to="/" className="nav-link">
              ← Back to Upload
            </Link>
          )}
          {location.pathname.startsWith('/compare') && (
            <Link to="/candidates" className="nav-link">
              ← Back to Candidates
            </Link>
          )}
        </nav>
      </div>
    </header>
  )
}

export default Header

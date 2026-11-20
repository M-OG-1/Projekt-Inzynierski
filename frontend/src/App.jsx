import AdminDashboard from './dashboard/AdminDashboard.jsx'
import AuthPage from './auth/AuthPage.jsx'
import Dashboard from './dashboard/Dashboard.jsx'

export default function App() {
  const path = window.location.pathname

  if (path === '/admin') {
    return <AdminDashboard />
  }

  if (path === '/home') {
    return <Dashboard />
  }

  return <AuthPage />
}
import { useState } from 'react'
import AuthSwitch from './AuthSwitch.jsx'
import RegisterForm from './RegisterForm.jsx'
import favicon from '../assets/favicon.ico'
import './Auth.css'

export default function AuthPage() {
  const [showRegister, setShowRegister] = useState(false)
  const [notice, setNotice] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleLogin(event) {
    event.preventDefault()

    const formData = new FormData(event.currentTarget)
    const login = formData.get('login').trim()

    setError('')
    setNotice('')

    if (!login) {
      setError('Podaj login.')
      return
    }

    formData.set('login', login)
    setIsSubmitting(true)

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        body: formData,
      })

      if (response.status === 401) {
        setError('Niepoprawny login lub hasło.')
        return
      }

      if (response.ok && new URL(response.url).pathname === '/home') {
        const accountResponse = await fetch('/api/own_data', {
          cache: 'no-store',
        })

        if (!accountResponse.ok || accountResponse.redirected) {
          setError('Zalogowano, ale nie udało się odczytać danych konta.')
          return
        }

        const account = await accountResponse.json()
        window.location.assign(account.perms >= 2 ? '/admin' : '/home')
        return
      }

      setError('Nie udało się zalogować. Spróbuj ponownie.')
    } catch {
      setError('Nie udało się dokończyć logowania. Spróbuj ponownie.')
    } finally {
      setIsSubmitting(false)
    }
  }

  function openRegister() {
    setError('')
    setNotice('')
    setShowRegister(true)
  }

  function handleRegisterSuccess() {
    setShowRegister(false)
    setNotice('Konto utworzone. Możesz się zalogować.')
  }

  if (showRegister) {
    return (
      <RegisterForm
        onBack={() => setShowRegister(false)}
        onSuccess={handleRegisterSuccess}
      />
    )
  }

  return (
    <main className="login-page">
      <section className="login-card" aria-labelledby="login-title">
        <img className="auth-logo" src={favicon} alt="" width={64} height={64} />
        <h1 id="login-title">Zaloguj się</h1>

        <AuthSwitch
          isRegister={false}
          disabled={isSubmitting}
          onRegister={openRegister}
        />

        {notice && <p role="status">{notice}</p>}

        <form className="login-form" onSubmit={handleLogin}>
          <label htmlFor="login">Login</label>
          <input
            id="login"
            name="login"
            autoComplete="username"
            required
          />

          <label htmlFor="password">Hasło</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
          />

          {error && <p className="login-error" role="alert">{error}</p>}

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Logowanie…' : 'Zaloguj się'}
          </button>
        </form>
      </section>
    </main>
  )
}
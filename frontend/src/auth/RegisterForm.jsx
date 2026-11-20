import { useState } from 'react'
import AuthSwitch from './AuthSwitch.jsx'

export default function RegisterForm({ onSuccess, onBack }) {
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleRegister(event) {
    event.preventDefault()
    setError('')

    const formData = new FormData(event.currentTarget)
    const login = formData.get('login').trim()

    if (!login) {
      setError('Podaj login.')
      return
    }

    formData.set('login', login)
    setIsSubmitting(true)

    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        body: formData,
      })

      if (response.status === 201) {
        onSuccess()
        return
      }

      if (response.status === 200) {
        setError('Nie udało się założyć konta. Login może być już zajęty.')
      } else {
        setError('Wystąpił błąd serwera. Spróbuj ponownie.')
      }
    } catch {
      setError('Nie udało się połączyć z serwerem.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="login-page">
      <section className="login-card" aria-labelledby="register-title">
         <h1 id="register-title">Zaloguj się</h1>

        <AuthSwitch
          isRegister
          disabled={isSubmitting}
          onLogin={onBack}
        />

        <form className="login-form" onSubmit={handleRegister}>
          <label htmlFor="register-login">Login</label>
          <input
            id="register-login"
            name="login"
            autoComplete="username"
            required
          />

          <label htmlFor="register-password">Hasło</label>
          <input
            id="register-password"
            name="password"
            type="password"
            autoComplete="new-password"
            required
          />

          {error && <p className="login-error" role="alert">{error}</p>}

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Tworzenie konta…' : 'Utwórz konto'}
          </button>
        </form>
      </section>
    </main>
  )
}
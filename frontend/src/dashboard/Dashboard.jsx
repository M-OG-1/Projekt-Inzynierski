import { useEffect, useState } from 'react'
import './Dashboard.css'

async function fetchDashboardData(path, signal) {
  const response = await fetch(path, { signal, cache: 'no-store' })

  if (
    response.status === 401 ||
    (response.redirected && new URL(response.url).pathname === '/')
  ) {
    window.location.replace('/')
    throw new Error('Sesja wygasła.')
  }

  if (!response.ok) {
    throw new Error('Nie udało się pobrać danych.')
  }

  return response.json()
}

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    const controller = new AbortController()

    async function loadDashboard() {
      try {
        const user = await fetchDashboardData('/api/own_data', controller.signal)
        const progress = await fetchDashboardData(
          '/api/own_module_progress',
          controller.signal,
        )

        setData({ user, progress })
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError('Nie udało się wczytać dashboardu.')
        }
      }
    }

    loadDashboard()
    return () => controller.abort()
  }, [])

  if (error) {
    return (
      <main className="dashboard">
        <p role="alert">{error}</p>
        <button type="button" onClick={() => window.location.reload()}>
          Spróbuj ponownie
        </button>
      </main>
    )
  }

  if (!data) {
    return <main className="dashboard" role="status">Wczytywanie dashboardu…</main>
  }

  const { user, progress } = data
  const isAdmin = user.perms > 1
  const completedModules = new Set(user.completed_modules ?? [])
  const progressByModule = progress ?? {}
  const moduleIds = [
    ...new Set([...Object.keys(progressByModule), ...completedModules]),
  ]

  return (
    <div className="dashboard-page">
      <header className="dashboard-topbar">
        <div className="dashboard-topbar-inner">
          <span className="dashboard-brand">Laboratorium sieciowe</span>

          <div className="dashboard-actions">

            {isAdmin && <a href="/admin">Panel administratora</a>}

            <form action="/api/logout" method="post">
              <button type="submit">Wyloguj się</button>
            </form>
          </div>
        </div>
      </header>

      <main className="dashboard">
        <header className="dashboard-overview">
          <h1>Witaj, {user.login}!</h1>

          <div className="dashboard-summary">
            <strong>{completedModules.size}</strong>
            <span>Ukończone moduły</span>
          </div>
        </header>

        <section aria-labelledby="dashboard-progress-title">
          <h2 id="dashboard-progress-title">Mój postęp</h2>

          {moduleIds.length === 0 ? (
            <p className="dashboard-empty">
              Nie masz jeszcze zapisanego postępu.
            </p>
          ) : (
            <div className="dashboard-grid">
              {moduleIds.map(moduleId => {
                const results = Object.values(progressByModule[moduleId] ?? {})
                const completedTasks = results.filter(result => result === true).length
                const isCompleted = completedModules.has(moduleId)
                const statusClass = isCompleted
                  ? 'dashboard-status is-complete'
                  : 'dashboard-status'

                return (
                  <article className="dashboard-card" key={moduleId}>
                    <div className="dashboard-card-heading">
                      <h3>{moduleId}</h3>
                      <span className={statusClass}>
                        {isCompleted ? 'Ukończony' : 'W trakcie'}
                      </span>
                    </div>

                    {results.length > 0 && (
                      <>
                        <p>{completedTasks} z {results.length} zadań</p>
                        <progress
                          aria-label={`Postęp modułu ${moduleId}`}
                          value={completedTasks}
                          max={results.length}
                        />
                      </>
                    )}
                  </article>
                )
              })}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}
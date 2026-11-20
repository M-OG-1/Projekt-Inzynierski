import { useState } from 'react'
import './AdminDashboard.css'

const sections = [
    {
        id: 'status',
        label: 'Status',
        description: 'Status serwisu',
    },
    {
        id: 'modules',
        label: 'Moduły',
        description: 'Opublikowane moduły dostępne użytkownikom',
    },
    {
        id: 'users',
        label: 'Użytkownicy',
        description: 'Konta platformy i przypisane im role.',
    },
    {
        id: 'database',
        label: 'Baza Danych',
        description: 'Dostęp i zarządzanie danymi',
    },
]

export default function AdminDashboard() {
  const [activeSection, setActiveSection] = useState(sections[0])

  return (
    <div className="admin-page">
      <header className="admin-topbar">
        <div className="admin-topbar-inner">
          <strong>Laboratorium sieciowe</strong>

          <div className="admin-actions">


            <form action="/api/logout" method="post">
              <button type="submit">Wyloguj się</button>
            </form>
          </div>
        </div>
      </header>

      <main className="admin-content">
        <h1>Panel administratora</h1>

        <div className="admin-layout">
          <nav className="admin-nav" aria-label="Sekcje panelu administratora">
            {sections.map(section => (
              <button
                key={section.id}
                type="button"
                aria-pressed={activeSection.id === section.id}
                onClick={() => setActiveSection(section)}
              >
                {section.label}
              </button>
            ))}
          </nav>

          <section className="admin-section" aria-labelledby="admin-section-title">
            <h2 id="admin-section-title">{activeSection.label}</h2>
            <p>{activeSection.description}</p>

          </section>
        </div>
      </main>
    </div>
  )
}
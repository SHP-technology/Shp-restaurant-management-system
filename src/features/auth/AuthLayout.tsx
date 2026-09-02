import type { ReactNode } from 'react'

export function AuthLayout({ children, eyebrow, title, description }: {
  children: ReactNode
  eyebrow: string
  title: string
  description: string
}) {
  return (
    <main className="auth-page">
      <section className="auth-visual" aria-label="Restaurant dining room">
        <div className="auth-visual-content">
          <p className="auth-brand">SHP <span>/</span> RESTAURANT OS</p>
          <h1>Good food.<br /><em>Great moments.</em></h1>
          <p className="auth-visual-copy">One calm command center for every table, order, and service.</p>
        </div>
        <p className="auth-visual-caption">Thoughtfully built for the people behind the pass.</p>
      </section>
      <section className="auth-form-panel">
        <div className="auth-form-wrap">
          <p className="auth-eyebrow">{eyebrow}</p>
          <h2>{title}</h2>
          <p className="auth-description">{description}</p>
          {children}
        </div>
      </section>
    </main>
  )
}
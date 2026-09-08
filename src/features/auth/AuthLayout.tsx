import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'

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
          <Link to="/" className="inline-flex items-center gap-2 text-xs font-bold text-white/90 hover:text-[#f47b20] transition mb-6">
            <ArrowLeft size={14} /> Back to Home
          </Link>
          <p className="auth-brand">SHP <span>/</span> RESTAURANT OS</p>
          <h1>Good food.<br /><em>Great moments.</em></h1>
          <p className="auth-visual-copy">{description}</p>
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
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the login screen when unauthenticated', () => {
    window.history.pushState({}, '', '/login')
    render(<App />)
    expect(screen.getByText(/Welcome back/i)).toBeInTheDocument()
  })
})

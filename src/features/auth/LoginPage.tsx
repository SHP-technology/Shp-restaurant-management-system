import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useAuthStore } from '../../store/authStore'
import { restroHandler } from '../../services/api'
import { AuthLayout } from './AuthLayout'

const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

type LoginFormValues = z.infer<typeof schema>

export function LoginPage() {
  const setSession = useAuthStore((state) => state.setSession)
  const navigate = useNavigate()
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<LoginFormValues>({
    resolver: zodResolver(schema),
    defaultValues: { email: 'admin@restaurant.com', password: 'password123' },
  })

  const onSubmit = async (values: LoginFormValues) => {
    setIsLoading(true)
    setErrorMessage(null)
    try {
      const data = await restroHandler.auth.login(values.email, values.password)
      setSession({
        user: data.user,
        accessToken: data.accessToken,
        refreshToken: data.refreshToken,
      })
      navigate('/admin')
    } catch (err) {
      setErrorMessage(restroHandler.getErrorMessage(err))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <AuthLayout
      eyebrow="Welcome back"
      title="Sign in to your workspace"
      description="Your service is waiting. Pick up right where you left off."
    >
      <form className="auth-form" onSubmit={form.handleSubmit(onSubmit)}>
        {errorMessage && (
          <div className="rounded-lg bg-rose-50 border border-rose-200 p-3 text-xs text-rose-700 font-medium">
            {errorMessage}
          </div>
        )}
        <div>
          <label className="auth-label">Email</label>
          <input
            type="email"
            className="auth-input"
            placeholder="admin@restaurant.com"
            {...form.register('email')}
          />
          {form.formState.errors.email && (
            <p className="mt-2 text-xs font-semibold text-rose-500">
              {form.formState.errors.email.message}
            </p>
          )}
        </div>

        <div>
          <label className="auth-label">Password</label>
          <input
            type="password"
            className="auth-input"
            placeholder="••••••••"
            {...form.register('password')}
          />
          {form.formState.errors.password && (
            <p className="mt-2 text-xs font-semibold text-rose-500">
              {form.formState.errors.password.message}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="auth-submit disabled:opacity-50"
        >
          {isLoading ? 'Signing In...' : 'Sign In'}
        </button>
      </form>

      <p className="auth-switch">
        New to Restaurant OS?{' '}
        <Link className="auth-link" to="/signup">
          Create an account
        </Link>
      </p>
    </AuthLayout>
  )
}

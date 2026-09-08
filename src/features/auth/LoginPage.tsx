import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useAuthStore } from '../../store/authStore'
import { AuthLayout } from './AuthLayout'

const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

type LoginFormValues = z.infer<typeof schema>

export function LoginPage() {
  const setSession = useAuthStore((state) => state.setSession)
  const navigate = useNavigate()

  const form = useForm<LoginFormValues>({
    resolver: zodResolver(schema),
    defaultValues: { email: 'admin@restaurant.com', password: 'password123' },
  })

  const onSubmit = (values: LoginFormValues) => {
    setSession({
      user: {
        id: 'demo-user',
        name: 'Restaurant Admin',
        email: values.email,
        role: 'admin',
      },
      accessToken: 'demo-access-token',
      refreshToken: 'demo-refresh-token',
    })

    navigate('/admin')
  }

  return (
    <AuthLayout
      eyebrow="Welcome back"
      title="Sign in to your workspace"
      description="Your service is waiting. Pick up right where you left off."
    >
      <form className="auth-form" onSubmit={form.handleSubmit(onSubmit)}>
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
          className="auth-submit"
        >
          Sign In
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

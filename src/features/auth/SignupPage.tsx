import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useAuthStore } from '../../store/authStore'
import { restroHandler } from '../../services/api'
import { AuthLayout } from './AuthLayout'

const schema = z
  .object({
    name: z.string().min(2, 'Enter your full name'),
    email: z.string().email('Enter a valid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
    confirmPassword: z.string(),
  })
  .refine((values) => values.password === values.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  })

type SignupFormValues = z.infer<typeof schema>

export function SignupPage() {
  const setSession = useAuthStore((state) => state.setSession)
  const navigate = useNavigate()
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<SignupFormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', email: '', password: '', confirmPassword: '' },
  })

  const onSubmit = async (values: SignupFormValues) => {
    setIsLoading(true)
    setErrorMessage(null)
    try {
      const data = await restroHandler.auth.signup({
        name: values.name,
        email: values.email,
        password: values.password,
      })
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
      eyebrow="New workspace"
      title="Make service feel effortless"
      description="Create your restaurant workspace and bring your team together."
    >
      <form className="auth-form" onSubmit={form.handleSubmit(onSubmit)}>
        {errorMessage && (
          <div className="rounded-lg bg-rose-50 border border-rose-200 p-3 text-xs text-rose-700 font-medium">
            {errorMessage}
          </div>
        )}
        <Field label="Full name" error={form.formState.errors.name?.message}>
          <input className="auth-input" placeholder="Alex Morgan" {...form.register('name')} />
        </Field>
        <Field label="Work email" error={form.formState.errors.email?.message}>
          <input type="email" className="auth-input" placeholder="alex@restaurant.com" {...form.register('email')} />
        </Field>
        <Field label="Password" error={form.formState.errors.password?.message}>
          <input type="password" className="auth-input" placeholder="At least 6 characters" {...form.register('password')} />
        </Field>
        <Field label="Confirm password" error={form.formState.errors.confirmPassword?.message}>
          <input type="password" className="auth-input" placeholder="Repeat your password" {...form.register('confirmPassword')} />
        </Field>

        <button
          type="submit"
          disabled={isLoading}
          className="auth-submit disabled:opacity-50"
        >
          {isLoading ? 'Creating Workspace...' : 'Create workspace'}
        </button>
      </form>

      <p className="auth-switch">
        Already have an account?{' '}
        <Link className="auth-link" to="/login">
          Sign in
        </Link>
      </p>
    </AuthLayout>
  )
}

function Field({ label, error, children }: { label: string; error?: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="auth-label">{label}</label>
      {children}
      {error && <p className="mt-2 text-xs font-semibold text-rose-500">{error}</p>}
    </div>
  )
}
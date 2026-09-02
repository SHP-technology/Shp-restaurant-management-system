import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useAuthStore } from '../../store/authStore'
import { AuthLayout } from './AuthLayout'

const schema = z
  .object({
    name: z.string().min(2, 'Enter your name'),
    email: z.string().email('Enter a valid email'),
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
  const form = useForm<SignupFormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', email: '', password: '', confirmPassword: '' },
  })

  const onSubmit = (values: SignupFormValues) => {
    setSession({
      user: { id: 'demo-user', name: values.name, email: values.email, role: 'admin' },
      accessToken: 'demo-access-token',
      refreshToken: 'demo-refresh-token',
    })
    navigate('/admin')
  }

  return (
    <AuthLayout eyebrow="New workspace" title="Make service feel effortless" description="Create your restaurant workspace and bring your team together.">

      <form className="auth-form" onSubmit={form.handleSubmit(onSubmit)}>
          <Field label="Full name" error={form.formState.errors.name?.message}>
            <input className={inputClass} placeholder="Alex Morgan" {...form.register('name')} />
          </Field>
          <Field label="Work email" error={form.formState.errors.email?.message}>
            <input type="email" className={inputClass} placeholder="alex@restaurant.com" {...form.register('email')} />
          </Field>
          <Field label="Password" error={form.formState.errors.password?.message}>
            <input type="password" className={inputClass} placeholder="At least 6 characters" {...form.register('password')} />
          </Field>
          <Field label="Confirm password" error={form.formState.errors.confirmPassword?.message}>
            <input type="password" className={inputClass} placeholder="Repeat your password" {...form.register('confirmPassword')} />
          </Field>
          <button type="submit" className="w-full rounded-lg bg-amber-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-amber-400">
            Create workspace
          </button>
      </form>

      <p className="auth-switch">
          Already have an account?{' '}
        <Link className="auth-link" to="/login">Sign in</Link>
      </p>
    </AuthLayout>
  )
}

const inputClass = 'auth-input'

function Field({ label, error, children }: { label: string; error?: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="auth-label">{label}</label>
      {children}
      {error && <p className="mt-2 text-sm text-rose-400">{error}</p>}
    </div>
  )
}
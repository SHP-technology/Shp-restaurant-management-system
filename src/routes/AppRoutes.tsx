import { lazy, Suspense } from 'react'
import { Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { PageTransition } from '../components/PageTransition'
import { useAuthStore } from '../store/authStore'

// Lazy loaded page components for optimized bundle splitting
const LandingPage = lazy(() =>
  import('../pages/LandingPage').then((m) => ({ default: m.LandingPage }))
)
const MenuPage = lazy(() =>
  import('../pages/MenuPage').then((m) => ({ default: m.MenuPage }))
)
const BookingPage = lazy(() =>
  import('../pages/BookingPage').then((m) => ({ default: m.BookingPage }))
)
const DeliveryPage = lazy(() =>
  import('../pages/DeliveryPage').then((m) => ({ default: m.DeliveryPage }))
)
const PartyBookingPage = lazy(() =>
  import('../pages/PartyBookingPage').then((m) => ({ default: m.PartyBookingPage }))
)
const OffersPage = lazy(() =>
  import('../pages/OffersPage').then((m) => ({ default: m.OffersPage }))
)
const ContactPage = lazy(() =>
  import('../pages/ContactPage').then((m) => ({ default: m.ContactPage }))
)
const LoginPage = lazy(() =>
  import('../features/auth/LoginPage').then((m) => ({ default: m.LoginPage }))
)
const SignupPage = lazy(() =>
  import('../features/auth/SignupPage').then((m) => ({ default: m.SignupPage }))
)
const DashboardPage = lazy(() =>
  import('../features/dashboard/DashboardPage').then((m) => ({ default: m.DashboardPage }))
)

function LoadingFallback() {
  return (
    <div className="min-h-[70vh] flex items-center justify-center">
      <div className="flex flex-col items-center gap-3">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-[#f47b20] border-t-transparent" />
        <span className="text-xs font-semibold text-gray-500">Loading experience...</span>
      </div>
    </div>
  )
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const user = useAuthStore((state) => state.user)

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

export function AppRoutes() {
  const location = useLocation()

  return (
    <Suspense fallback={<LoadingFallback />}>
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route
            path="/"
            element={
              <PageTransition>
                <LandingPage />
              </PageTransition>
            }
          />
          <Route
            path="/menu"
            element={
              <PageTransition>
                <MenuPage />
              </PageTransition>
            }
          />
          <Route
            path="/booking"
            element={
              <PageTransition>
                <BookingPage />
              </PageTransition>
            }
          />
          <Route
            path="/delivery"
            element={
              <PageTransition>
                <DeliveryPage />
              </PageTransition>
            }
          />
          <Route
            path="/party-booking"
            element={
              <PageTransition>
                <PartyBookingPage />
              </PageTransition>
            }
          />
          <Route
            path="/offers"
            element={
              <PageTransition>
                <OffersPage />
              </PageTransition>
            }
          />
          <Route
            path="/contact"
            element={
              <PageTransition>
                <ContactPage />
              </PageTransition>
            }
          />
          <Route
            path="/login"
            element={
              <PageTransition>
                <LoginPage />
              </PageTransition>
            }
          />
          <Route
            path="/signup"
            element={
              <PageTransition>
                <SignupPage />
              </PageTransition>
            }
          />
          <Route
            path="/admin/*"
            element={
              <ProtectedRoute>
                <PageTransition>
                  <DashboardPage />
                </PageTransition>
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AnimatePresence>
    </Suspense>
  )
}

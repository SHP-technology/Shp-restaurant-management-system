import { Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { LoginPage } from '../features/auth/LoginPage'
import { SignupPage } from '../features/auth/SignupPage'
import { DashboardPage } from '../features/dashboard/DashboardPage'
import { LandingPage } from '../pages/LandingPage'
import { MenuPage } from '../pages/MenuPage'
import { BookingPage } from '../pages/BookingPage'
import { DeliveryPage } from '../pages/DeliveryPage'
import { PartyBookingPage } from '../pages/PartyBookingPage'
import { OffersPage } from '../pages/OffersPage'
import { ContactPage } from '../pages/ContactPage'
import { PageTransition } from '../components/PageTransition'
import { useAuthStore } from '../store/authStore'

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
  )
}

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../pages/LandingPage.vue'),
  },
  {
    path: '/menu',
    name: 'Menu',
    component: () => import('../pages/MenuPage.vue'),
  },
  {
    path: '/booking',
    name: 'Booking',
    component: () => import('../pages/BookingPage.vue'),
  },
  {
    path: '/delivery',
    name: 'Delivery',
    component: () => import('../pages/DeliveryPage.vue'),
  },
  {
    path: '/party-booking',
    name: 'PartyBooking',
    component: () => import('../pages/PartyBookingPage.vue'),
  },
  {
    path: '/offers',
    name: 'Offers',
    component: () => import('../pages/OffersPage.vue'),
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../pages/ContactPage.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../features/auth/LoginPage.vue'),
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('../features/auth/SignupPage.vue'),
  },
  {
    path: '/admin/:pathMatch(.*)*',
    name: 'Dashboard',
    component: () => import('../features/dashboard/DashboardPage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

const STAFF_ROLES = ['admin', 'manager', 'waiter', 'kitchen']

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  if (!to.meta.requiresAuth) {
    next()
    return
  }
  if (!authStore.accessToken) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }
  // Admin/POS area is staff-only; a plain customer account must not reach it.
  const role = authStore.user?.role
  if (role && !STAFF_ROLES.includes(role)) {
    next({ name: 'Home' })
    return
  }
  next()
})

export default router

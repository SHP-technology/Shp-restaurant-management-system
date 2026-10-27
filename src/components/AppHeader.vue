<template>
  <header
    class="sticky top-0 left-0 w-full h-[68px] sm:h-[72px] z-50 bg-white/95 backdrop-blur-md transition-all duration-300 border-b border-slate-200/80"
    :class="{ 'shadow-md shadow-slate-900/5': isScrolled }"
  >
    <!-- Top Accent Line -->
    <div class="absolute top-0 left-0 w-full h-[3px] bg-linear-to-r from-orange-500 via-amber-500 to-orange-500" />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-full flex items-center justify-between">
      <!-- App Logo (Exact Style Reference) -->
      <RouterLink to="/" class="inline-flex items-center gap-2.5 group select-none focus:outline-hidden" aria-label="SHP Restro Home">
        <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-linear-to-tr from-orange-500 to-amber-500 flex items-center justify-center text-white font-bold text-lg shadow-sm group-hover:scale-105 transition-transform shrink-0">
          🍽️
        </div>
        <div class="flex flex-col">
          <span class="font-extrabold text-lg sm:text-xl tracking-tight text-slate-900 group-hover:text-orange-600 transition-colors leading-tight">
            SHP<span class="text-orange-600">.</span>
          </span>
          <span class="text-[10px] font-semibold tracking-widest text-slate-400 uppercase -mt-0.5">
            Restro
          </span>
        </div>
      </RouterLink>

      <!-- Desktop Navigation (Compact & Crisp) -->
      <nav class="hidden lg:flex items-center gap-7 xl:gap-8" aria-label="Main Navigation">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="text-sm font-semibold transition-colors py-2 relative flex items-center gap-1.5"
          :class="[
            isActive(item.path)
              ? 'text-slate-900 font-bold'
              : 'text-slate-600 hover:text-orange-600'
          ]"
        >
          <span>{{ item.label }}</span>
          <span
            v-if="item.badge"
            class="text-[10px] font-bold px-1.5 py-0.2 rounded-full"
            :class="item.badge === 'Hot' ? 'bg-orange-100 text-orange-600' : 'bg-emerald-100 text-emerald-700'"
          >
            {{ item.badge }}
          </span>
          <!-- Active Line Indicator -->
          <span
            v-if="isActive(item.path)"
            class="absolute bottom-0 left-0 w-full h-[2.5px] bg-linear-to-r from-orange-500 to-amber-500 rounded-full"
          />
        </RouterLink>
      </nav>

      <!-- Desktop Right Controls (Compact sm buttons) -->
      <div class="hidden lg:flex items-center gap-3">
        <!-- Order Button (Compact sm size) -->
        <RouterLink
          to="/delivery"
          class="inline-flex items-center justify-center font-bold text-xs rounded-xl px-3.5 py-2 gap-1.5 bg-orange-600 hover:bg-orange-700 text-white shadow-sm shadow-orange-600/20 active:scale-[0.98] transition-all cursor-pointer"
        >
          <span>Order Online</span>
          <span
            v-if="cartStore.totalCount > 0"
            class="bg-white text-orange-600 text-[10px] font-extrabold px-1.5 py-0.2 rounded-full"
          >
            {{ cartStore.totalCount }}
          </span>
          <ArrowRight :size="14" />
        </RouterLink>

        <!-- Staff / User Account State -->
        <div v-if="authStore.user" class="flex items-center gap-2 pl-2 border-l border-slate-200">
          <RouterLink
            v-if="['admin', 'manager', 'waiter', 'kitchen'].includes(authStore.user.role)"
            to="/admin"
            class="text-xs font-bold text-slate-700 hover:text-orange-600 px-2.5 py-1.5 rounded-lg hover:bg-slate-100 transition-colors flex items-center gap-1.5"
          >
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>POS</span>
          </RouterLink>

          <div class="flex items-center gap-1.5 bg-slate-50 border border-slate-200 px-2 py-1 rounded-lg text-xs font-semibold text-slate-700">
            <span class="max-w-[70px] truncate text-[11px]">{{ authStore.user.name || 'Staff' }}</span>
            <button
              @click="handleLogout"
              class="text-slate-400 hover:text-red-600 transition-colors p-0.5"
              title="Sign Out"
              aria-label="Sign Out"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>

        <RouterLink
          v-else
          to="/login"
          class="text-xs font-semibold text-slate-600 hover:text-orange-600 px-2.5 py-1.5 transition-colors"
        >
          Sign In
        </RouterLink>
      </div>

      <!-- Mobile Controls Header Bar -->
      <div class="flex items-center gap-2 lg:hidden">
        <RouterLink
          to="/delivery"
          class="hidden sm:inline-flex items-center justify-center font-bold text-xs rounded-xl px-3 py-1.5 gap-1 bg-orange-600 text-white shadow-xs active:scale-[0.98] transition-all shrink-0"
        >
          <span>Order</span>
          <span
            v-if="cartStore.totalCount > 0"
            class="bg-white text-orange-600 text-[10px] font-extrabold px-1.5 py-0.2 rounded-full"
          >
            {{ cartStore.totalCount }}
          </span>
          <ArrowRight :size="13" />
        </RouterLink>

        <!-- Mobile Menu Toggle Button -->
        <button
          type="button"
          class="w-10 h-10 rounded-xl border border-slate-200 text-slate-900 bg-slate-50 flex items-center justify-center cursor-pointer active:scale-95 transition-transform select-none shrink-0 hover:bg-slate-100"
          :aria-expanded="mobileMenuOpen"
          aria-label="Open navigation menu"
          @click="setMobileMenuOpen(true)"
        >
          <Menu :size="18" />
        </button>
      </div>
    </div>
  </header>

  <!-- Mobile Fullscreen Navigation Modal - z-[99999] (Direct Reference from main_website) -->
  <transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0 translate-y-2"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100 translate-y-0"
    leave-to-class="opacity-0 translate-y-2"
  >
    <div
      v-if="mobileMenuOpen"
      class="fixed inset-0 z-[99999] bg-white text-slate-900 flex flex-col lg:hidden"
    >
      <!-- Top Accent Line -->
      <div class="absolute top-0 left-0 w-full h-[3px] bg-linear-to-r from-orange-500 via-amber-500 to-orange-500" />

      <!-- Mobile Top Bar -->
      <div class="h-[68px] sm:h-[72px] px-4 sm:px-6 border-b border-slate-200 flex items-center justify-between bg-white/95 backdrop-blur-md shrink-0">
        <RouterLink to="/" class="inline-flex items-center gap-2 select-none" @click="setMobileMenuOpen(false)">
          <div class="w-8 h-8 rounded-xl bg-linear-to-tr from-orange-500 to-amber-500 flex items-center justify-center text-white font-bold text-base shadow-sm">
            🍽️
          </div>
          <span class="font-extrabold text-lg tracking-tight text-slate-900">
            SHP<span class="text-orange-600">.</span> <span class="text-sm font-semibold text-slate-500">Restro</span>
          </span>
        </RouterLink>

        <!-- Close Button -->
        <button
          type="button"
          class="w-10 h-10 rounded-xl border border-slate-200 text-slate-900 bg-slate-50 flex items-center justify-center cursor-pointer active:scale-95 transition-transform select-none shrink-0 hover:bg-slate-100"
          aria-label="Close navigation menu"
          @click="setMobileMenuOpen(false)"
        >
          <X :size="18" />
        </button>
      </div>

      <!-- Mobile Scrollable Content -->
      <div class="flex-1 p-5 overflow-y-auto flex flex-col justify-between gap-6">
        <div class="flex flex-col gap-4">
          <!-- Auth User Info if signed in -->
          <div v-if="authStore.user" class="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-orange-600 text-white flex items-center justify-center font-bold text-xs">
                {{ getUserInitial() }}
              </div>
              <div>
                <div class="text-xs font-bold text-slate-900">{{ authStore.user.name || 'Staff' }}</div>
                <div class="text-[11px] text-slate-500 capitalize">{{ authStore.user.role }}</div>
              </div>
            </div>
            <button
              @click="handleLogout"
              class="text-xs font-semibold text-red-600 hover:text-red-700 px-2 py-1"
            >
              Sign Out
            </button>
          </div>

          <span class="text-xs font-bold uppercase tracking-wider text-slate-400 px-2">Navigation</span>
          <nav class="flex flex-col gap-1" aria-label="Mobile navigation">
            <RouterLink
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              class="text-base font-bold py-3 px-4 rounded-xl transition-all border-b border-slate-100 flex items-center justify-between"
              :class="[
                isActive(item.path)
                  ? 'bg-orange-50 text-orange-600 border-orange-200/50'
                  : 'text-slate-800 hover:bg-slate-50'
              ]"
              @click="setMobileMenuOpen(false)"
            >
              <div class="flex items-center gap-2">
                <span>{{ item.label }}</span>
                <span
                  v-if="item.badge"
                  class="text-[10px] font-bold px-1.5 py-0.2 rounded-full"
                  :class="item.badge === 'Hot' ? 'bg-orange-100 text-orange-600' : 'bg-emerald-100 text-emerald-700'"
                >
                  {{ item.badge }}
                </span>
              </div>
              <ArrowRight :size="16" class="text-slate-400" />
            </RouterLink>
          </nav>
        </div>

        <!-- Mobile Bottom Call-To-Actions (Exact main_website style) -->
        <div class="flex flex-col gap-2.5 pt-4 border-t border-slate-200 mt-auto">
          <RouterLink
            to="/delivery"
            class="w-full py-3 px-4 rounded-xl bg-orange-600 hover:bg-orange-700 text-white font-bold text-sm flex items-center justify-center gap-2 transition-colors shadow-sm shadow-orange-600/20 active:scale-[0.98]"
            @click="setMobileMenuOpen(false)"
          >
            <span>Order Online</span>
            <span
              v-if="cartStore.totalCount > 0"
              class="bg-white text-orange-600 text-xs font-black px-1.5 py-0.2 rounded-full"
            >
              {{ cartStore.totalCount }}
            </span>
            <ArrowRight :size="16" />
          </RouterLink>

          <RouterLink
            to="/booking"
            class="w-full py-2.5 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs flex items-center justify-center gap-1.5 transition-colors border border-slate-200 active:scale-[0.98]"
            @click="setMobileMenuOpen(false)"
          >
            <span>Book a Table</span>
          </RouterLink>

          <!-- Staff POS if logged in -->
          <RouterLink
            v-if="authStore.user && ['admin', 'manager', 'waiter', 'kitchen'].includes(authStore.user.role)"
            to="/admin"
            class="w-full py-2 px-4 rounded-xl bg-amber-50 text-amber-800 font-semibold text-xs text-center border border-amber-200"
            @click="setMobileMenuOpen(false)"
          >
            Open POS Dashboard →
          </RouterLink>

          <!-- Sign in link if guest -->
          <RouterLink
            v-if="!authStore.user"
            to="/login"
            class="text-center text-xs font-medium text-slate-500 hover:text-orange-600 py-1"
            @click="setMobileMenuOpen(false)"
          >
            Staff Sign In →
          </RouterLink>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { Menu, X, ArrowRight } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)

const navItems = [
  { label: 'Home', path: '/' },
  { label: 'Menu', path: '/menu' },
  { label: 'Delivery', path: '/delivery', badge: 'Fast' },
  { label: 'Book Table', path: '/booking' },
  { label: 'Parties', path: '/party-booking' },
  { label: 'Offers', path: '/offers', badge: 'Hot' },
  { label: 'Contact', path: '/contact' },
]

function isActive(path: string) {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

function getUserInitial() {
  if (authStore.user?.name) {
    return authStore.user.name.charAt(0).toUpperCase()
  }
  if (authStore.user?.email) {
    return authStore.user.email.charAt(0).toUpperCase()
  }
  return 'U'
}

function setMobileMenuOpen(open: boolean) {
  mobileMenuOpen.value = open
}

function handleScroll() {
  isScrolled.value = window.scrollY > 20
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && mobileMenuOpen.value) {
    setMobileMenuOpen(false)
  }
}

watch(mobileMenuOpen, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onMounted(() => {
  handleScroll()
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
})

function handleLogout() {
  authStore.clearSession()
  setMobileMenuOpen(false)
  router.push('/login')
}
</script>

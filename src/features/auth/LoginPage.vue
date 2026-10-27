<template>
  <AuthLayout
    eyebrow="Staff & Management Portal"
    title="Sign in to Restaurant OS"
    description="Manage real-time table orders, KDS live kitchen tickets, delivery dispatch, and analytics."
  >
    <form class="space-y-4" @submit.prevent="handleSubmit">
      <!-- Error Message Alert -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 -translate-y-1"
        enter-to-class="opacity-100 translate-y-0"
      >
        <div
          v-if="errorMessage"
          class="rounded-xl bg-rose-50 border border-rose-200 p-3.5 text-xs text-rose-700 font-semibold flex items-center gap-2"
        >
          <AlertCircle :size="16" class="shrink-0 text-rose-500" />
          <span>{{ errorMessage }}</span>
        </div>
      </transition>

      <!-- Email Field -->
      <div>
        <label class="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">
          Email Address
        </label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
            <Mail :size="16" />
          </div>
          <input
            v-model="email"
            type="email"
            required
            autocomplete="email"
            class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 text-sm focus:border-[#f47b20] focus:ring-2 focus:ring-[#f47b20]/20 focus:outline-hidden transition-all placeholder:text-gray-400 min-h-[44px]"
            placeholder="admin@restaurant.com"
          />
        </div>
      </div>

      <!-- Password Field -->
      <div>
        <div class="flex items-center justify-between mb-1.5">
          <label class="block text-xs font-bold text-gray-700 uppercase tracking-wider">
            Password
          </label>
        </div>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
            <Lock :size="16" />
          </div>
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            required
            autocomplete="current-password"
            class="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 text-sm focus:border-[#f47b20] focus:ring-2 focus:ring-[#f47b20]/20 focus:outline-hidden transition-all placeholder:text-gray-400 min-h-[44px]"
            placeholder="••••••••"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-gray-600 focus:outline-hidden"
            aria-label="Toggle password visibility"
          >
            <EyeOff v-if="showPassword" :size="16" />
            <Eye v-else :size="16" />
          </button>
        </div>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="isLoading"
        class="w-full orange-button py-3.5 px-4 rounded-xl font-bold text-sm shadow-md flex items-center justify-center gap-2 min-h-[46px] disabled:opacity-60 cursor-pointer mt-2"
      >
        <Loader2 v-if="isLoading" :size="18" class="animate-spin" />
        <span>{{ isLoading ? 'Authenticating...' : 'Sign In to Workspace' }}</span>
      </button>
    </form>

    <div class="mt-6 pt-4 border-t border-gray-100 text-center">
      <p class="text-xs text-gray-500">
        Need a new restaurant staff account?
        <RouterLink class="font-bold text-[#f47b20] hover:underline ml-1" to="/signup">
          Create Workspace Account
        </RouterLink>
      </p>
    </div>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { Mail, Lock, Eye, EyeOff, AlertCircle, Loader2 } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { restroHandler } from '../../services/api'
import AuthLayout from './AuthLayout.vue'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const errorMessage = ref<string | null>(null)
const isLoading = ref(false)

async function handleSubmit() {
  isLoading.value = true
  errorMessage.value = null
  try {
    const data = await restroHandler.auth.login(email.value, password.value)
    authStore.setSession({
      user: data.user,
      accessToken: data.accessToken,
      refreshToken: data.refreshToken,
    })
    router.push('/admin')
  } catch (err) {
    errorMessage.value = restroHandler.getErrorMessage(err)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <AuthLayout
    eyebrow="Welcome back"
    title="Sign in to your workspace"
    description="Your service is waiting. Pick up right where you left off."
  >
    <form class="auth-form" @submit.prevent="handleSubmit">
      <div v-if="errorMessage" class="rounded-lg bg-rose-50 border border-rose-200 p-3 text-xs text-rose-700 font-medium">
        {{ errorMessage }}
      </div>

      <div>
        <label class="auth-label">Email</label>
        <input
          v-model="email"
          type="email"
          required
          class="auth-input"
          placeholder="admin@restaurant.com"
        />
      </div>

      <div>
        <label class="auth-label">Password</label>
        <input
          v-model="password"
          type="password"
          required
          class="auth-input"
          placeholder="••••••••"
        />
      </div>

      <button
        type="submit"
        :disabled="isLoading"
        class="auth-submit disabled:opacity-50"
      >
        {{ isLoading ? 'Signing In...' : 'Sign In' }}
      </button>
    </form>

    <p class="auth-switch">
      New to Restaurant OS?
      <RouterLink class="auth-link" to="/signup">
        Create an account
      </RouterLink>
    </p>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { restroHandler } from '../../services/api'
import AuthLayout from './AuthLayout.vue'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('admin@restaurant.com')
const password = ref('password123')
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

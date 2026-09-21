<template>
  <AuthLayout
    eyebrow="New workspace"
    title="Make service feel effortless"
    description="Create your restaurant workspace and bring your team together."
  >
    <form class="auth-form" @submit.prevent="handleSubmit">
      <div v-if="errorMessage" class="rounded-lg bg-rose-50 border border-rose-200 p-3 text-xs text-rose-700 font-medium">
        {{ errorMessage }}
      </div>

      <div>
        <label class="auth-label">Full name</label>
        <input
          v-model="name"
          type="text"
          required
          class="auth-input"
          placeholder="Alex Morgan"
        />
      </div>

      <div>
        <label class="auth-label">Work email</label>
        <input
          v-model="email"
          type="email"
          required
          class="auth-input"
          placeholder="alex@restaurant.com"
        />
      </div>

      <div>
        <label class="auth-label">Password</label>
        <input
          v-model="password"
          type="password"
          required
          minlength="6"
          class="auth-input"
          placeholder="At least 6 characters"
        />
      </div>

      <div>
        <label class="auth-label">Confirm password</label>
        <input
          v-model="confirmPassword"
          type="password"
          required
          minlength="6"
          class="auth-input"
          placeholder="Repeat your password"
        />
      </div>

      <button
        type="submit"
        :disabled="isLoading"
        class="auth-submit disabled:opacity-50"
      >
        {{ isLoading ? 'Creating Workspace...' : 'Create workspace' }}
      </button>
    </form>

    <p class="auth-switch">
      Already have an account?
      <RouterLink class="auth-link" to="/login">
        Sign in
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

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref<string | null>(null)
const isLoading = ref(false)

async function handleSubmit() {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match.'
    return
  }
  isLoading.value = true
  errorMessage.value = null
  try {
    const data = await restroHandler.auth.signup({
      name: name.value,
      email: email.value,
      password: password.value,
    })
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

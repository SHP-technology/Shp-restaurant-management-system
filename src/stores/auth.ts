import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserSession } from '../types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserSession | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('accessToken'))
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))

  const rawUser = localStorage.getItem('user')
  if (rawUser) {
    try {
      user.value = JSON.parse(rawUser)
    } catch {
      user.value = null
    }
  }

  function setSession(session: { user: UserSession; accessToken: string; refreshToken: string }) {
    user.value = session.user
    accessToken.value = session.accessToken
    refreshToken.value = session.refreshToken
    localStorage.setItem('accessToken', session.accessToken)
    localStorage.setItem('refreshToken', session.refreshToken)
    localStorage.setItem('user', JSON.stringify(session.user))
  }

  function clearSession() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
  }

  return {
    user,
    accessToken,
    refreshToken,
    setSession,
    clearSession,
  }
})

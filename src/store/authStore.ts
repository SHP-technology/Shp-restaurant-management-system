import { create } from 'zustand'
import type { UserSession } from '../types'

type AuthState = {
  user: UserSession | null
  accessToken: string | null
  refreshToken: string | null
  setSession: (session: { user: UserSession; accessToken: string; refreshToken: string }) => void
  clearSession: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  setSession: ({ user, accessToken, refreshToken }) => set({ user, accessToken, refreshToken }),
  clearSession: () => set({ user: null, accessToken: null, refreshToken: null }),
}))

import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

const clearSessionAndRedirect = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('user')
  if (!window.location.pathname.includes('/login')) {
    window.location.href = '/login'
  }
}

// Single-flight refresh: concurrent 401s share one refresh request.
let refreshPromise: Promise<string> | null = null

const refreshAccessToken = async (): Promise<string> => {
  const refreshToken = localStorage.getItem('refreshToken')
  if (!refreshToken) throw new Error('No refresh token')

  // Bare axios (not `api`) so this request skips the interceptors below.
  const { data } = await axios.post(`${API_BASE_URL}/auth/refresh`, { refreshToken })
  const newAccess: string = data.accessToken ?? data.access
  if (!newAccess) throw new Error('No access token in refresh response')

  localStorage.setItem('accessToken', newAccess)
  if (data.refreshToken) localStorage.setItem('refreshToken', data.refreshToken)
  return newAccess
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as (InternalAxiosRequestConfig & { _retry?: boolean }) | undefined
    const status = error.response?.status
    const isAuthEndpoint = original?.url?.includes('/auth/')

    if (status === 401 && original && !original._retry && !isAuthEndpoint) {
      original._retry = true
      try {
        refreshPromise = refreshPromise ?? refreshAccessToken()
        const newAccess = await refreshPromise
        refreshPromise = null
        original.headers.set('Authorization', `Bearer ${newAccess}`)
        return api(original)
      } catch (refreshError) {
        refreshPromise = null
        clearSessionAndRedirect()
        return Promise.reject(refreshError)
      }
    }

    if (status === 401 && !isAuthEndpoint) {
      clearSessionAndRedirect()
    }
    return Promise.reject(error)
  }
)

export const getApiErrorMessage = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    return (
      error.response?.data?.detail ??
      error.response?.data?.message ??
      error.response?.data?.error ??
      error.message
    )
  }
  return 'An unexpected error occurred.'
}

export default api

import api from './client'

export const authApi = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },
  logout: async () => {
    const response = await api.post('/auth/logout')
    return response.data
  },
  me: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

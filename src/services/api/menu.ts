import api from './client'

export const menuApi = {
  list: async () => api.get('/menu'),
  getById: async (id: string) => api.get(`/menu/${id}`),
  create: async (payload: Record<string, unknown>) => api.post('/menu', payload),
}

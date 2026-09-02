import api from './client'

export const restaurantsApi = {
  list: async () => api.get('/restaurants'),
  getById: async (id: string) => api.get(`/restaurants/${id}`),
  create: async (payload: Record<string, unknown>) => api.post('/restaurants', payload),
}

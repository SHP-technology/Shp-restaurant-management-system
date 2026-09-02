import api from './client'

export const ordersApi = {
  list: async () => api.get('/orders'),
  getById: async (id: string) => api.get(`/orders/${id}`),
  create: async (payload: Record<string, unknown>) => api.post('/orders', payload),
  updateStatus: async (id: string, status: string) => api.patch(`/orders/${id}/status`, { status }),
}

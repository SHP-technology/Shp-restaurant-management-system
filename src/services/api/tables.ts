import api from './client'

export const tablesApi = {
  list: async () => api.get('/tables'),
  update: async (id: string, payload: Record<string, unknown>) => api.patch(`/tables/${id}`, payload),
}

import api from './client'

export const analyticsApi = {
  getDashboardStats: async () => api.get('/reports/dashboard'),
  exportCsvUrl: () => `${api.defaults.baseURL}/reports/export-csv`,
}

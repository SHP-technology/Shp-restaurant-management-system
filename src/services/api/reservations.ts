import api from './client'

export const reservationsApi = {
  listTableReservations: async () => api.get('/reservations/table-reservations'),
  createTableReservation: async (payload: Record<string, unknown>) =>
    api.post('/reservations/table-reservations', payload),

  listPartyBookings: async () => api.get('/reservations/party-bookings'),
  createPartyBooking: async (payload: Record<string, unknown>) =>
    api.post('/reservations/party-bookings', payload),
}

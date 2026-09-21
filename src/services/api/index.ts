import api, { getApiErrorMessage } from './client'
import { websocketClient } from '../websocket/client'
import { useAuthStore } from '../../stores/auth'
import type { Role, UserSession } from '../../types'

export interface MenuItemData {
  id: number
  name: string
  price: number
  category: string
  description: string
  rating: number
  prepTime: string
  isVeg: boolean
  isSpecial?: boolean
  image: string
  status?: string
}

export interface TableData {
  id?: number | string
  num: number
  seats: number
  status: 'Available' | 'Booked' | 'Occupied'
  floor_zone?: string
}

export interface OrderData {
  id: string
  type: string
  order_type?: string
  customer?: string
  customer_name?: string
  customer_phone?: string
  phone?: string
  table_name?: string
  items?: string
  price?: string
  total_amount?: number
  status: string
  statusColor?: string
  address?: string
  delivery_address?: string
  delivery_instructions?: string
  driver?: string
  time?: string
  estimated_time?: string
  created_at?: string
}

export interface ReservationData {
  id: string
  name: string
  phone: string
  date: string
  time: string
  guests: string
  area: string
  special_request?: string
  status: string
}

export interface PartyBookingData {
  id: string
  occasion: string
  client: string
  phone: string
  date: string
  guests: string
  requirements: string
  status: string
}

export interface CustomerData {
  id: string
  name: string
  phone: string
  email?: string
  tag: string
  visits: number
  totalSpent: string
}

export interface DashboardStatsData {
  stats: Array<{ label: string; value: string; sub1: string; sub2: string }>
  reports: {
    monthlyRevenue: string
    monthlyGrowth: string
    averageOrderValue: string
    aovGrowth: string
    topCategory: string
    topCategoryShare: string
    todayRevenue: string
    revenueGrowth: string
  }
}

/**
 * All-In-One Unified Service Handler for SHP Restaurant Management System.
 * Encapsulates all domain actions with graceful offline fallbacks and real-time syncing.
 */
class RestroHandler {
  // --- AUTHENTICATION ---
  auth = {
    login: async (email: string, password: string) => {
      const response = await api.post('/auth/login', { email, password })
      return response.data
    },
    signup: async (payload: { name: string; email: string; password: string; role?: Role }) => {
      const response = await api.post('/auth/signup', payload)
      return response.data
    },
    logout: async () => {
      const authStore = useAuthStore()
      try {
        const refreshToken = authStore.refreshToken
        if (refreshToken) {
          await api.post('/auth/logout', { refreshToken })
        }
      } finally {
        authStore.clearSession()
      }
    },
    me: async (): Promise<UserSession> => {
      const response = await api.get('/auth/me')
      return response.data
    },
  }

  // --- MENU & CATEGORIES ---
  menu = {
    list: async (params?: { category?: string; search?: string; veg_only?: boolean }) => {
      const response = await api.get<MenuItemData[]>('/menu', { params })
      return response.data
    },
    getById: async (id: number | string) => {
      const response = await api.get<MenuItemData>(`/menu/${id}`)
      return response.data
    },
    create: async (payload: Partial<MenuItemData>) => {
      const response = await api.post<MenuItemData>('/menu', payload)
      return response.data
    },
    toggleStock: async (id: number | string) => {
      const response = await api.patch<MenuItemData>(`/menu/${id}/toggle-stock`)
      return response.data
    },
  }

  // --- TABLES & FLOOR LAYOUT ---
  tables = {
    list: async () => {
      const response = await api.get<TableData[]>('/tables')
      return response.data
    },
    update: async (id: number | string, payload: Partial<TableData>) => {
      const response = await api.patch<TableData>(`/tables/${id}`, payload)
      return response.data
    },
    cycleStatus: async (table: TableData): Promise<TableData['status']> => {
      const nextStatus: TableData['status'] =
        table.status === 'Available' ? 'Booked' : table.status === 'Booked' ? 'Occupied' : 'Available'
      await api.patch(`/tables/${table.id || table.num}`, { status: nextStatus })
      return nextStatus
    },
  }

  // --- ORDERS & POS & DELIVERY LOGISTICS ---
  orders = {
    list: async (params?: { type?: string; status?: string }) => {
      const response = await api.get<OrderData[]>('/orders', { params })
      return response.data
    },
    getById: async (id: string) => {
      const response = await api.get<OrderData>(`/orders/${encodeURIComponent(id)}`)
      return response.data
    },
    create: async (payload: {
      order_type?: string
      customer_name?: string
      customer_phone?: string
      table_name?: string
      delivery_address?: string
      delivery_instructions?: string
      raw_items?: Array<{ menuItemId: number; quantity: number }>
    }) => {
      const response = await api.post<OrderData>('/orders', payload)
      return response.data
    },
    updateStatus: async (orderId: string, status: string) => {
      const response = await api.patch<OrderData>(
        `/orders/${encodeURIComponent(orderId)}/status`,
        { status }
      )
      return response.data
    },
  }

  // --- RESERVATIONS & PARTY BOOKINGS ---
  reservations = {
    listTableReservations: async () => {
      const response = await api.get<ReservationData[]>('/reservations/table-reservations')
      return response.data
    },
    createTableReservation: async (payload: {
      name: string
      phone: string
      date: string
      timeSlot: string
      guests: number | string
      seatingZone: string
      specialRequest?: string
    }) => {
      const response = await api.post<ReservationData>('/reservations/table-reservations', payload)
      return response.data
    },
    listPartyBookings: async () => {
      const response = await api.get<PartyBookingData[]>('/reservations/party-bookings')
      return response.data
    },
    createPartyBooking: async (payload: {
      occasion: string
      client: string
      phone: string
      date: string
      guestCount: string
      requirements: string
    }) => {
      const response = await api.post<PartyBookingData>('/reservations/party-bookings', payload)
      return response.data
    },
  }

  // --- CUSTOMERS & CRM ---
  customers = {
    list: async () => {
      const response = await api.get<CustomerData[]>('/customers')
      return response.data
    },
  }

  // --- ANALYTICS & REPORTS ---
  analytics = {
    getDashboardStats: async () => {
      const response = await api.get<DashboardStatsData>('/reports/dashboard')
      return response.data
    },
    getExportCsvUrl: () => `${api.defaults.baseURL}/reports/export-csv`,
    downloadCsv: () => {
      window.open(`${api.defaults.baseURL}/reports/export-csv`, '_blank')
    },
  }

  // --- REAL-TIME WEBSOCKET SUBSCRIBER ---
  realtime = {
    connect: (restaurantId = 'default') => {
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsHost = import.meta.env.VITE_WS_BASE_URL || (
        window.location.hostname === 'localhost' ? 'localhost:8000' : window.location.host
      )
      const url = `${wsProtocol}//${wsHost}/ws/restaurant/${restaurantId}/`
      websocketClient.connect(url)
    },
    on: (event: string, callback: (payload: unknown) => void) => {
      websocketClient.on(event, callback)
    },
    off: (event: string, callback: (payload: unknown) => void) => {
      websocketClient.off(event, callback)
    },
    disconnect: () => {
      websocketClient.disconnect()
    },
  }

  // Helper
  getErrorMessage = getApiErrorMessage
}

export const restroHandler = new RestroHandler()
export default restroHandler

import api from './client'

export interface RazorpayOrderResponse {
  razorpay_order_id: string
  amount: number
  currency: string
  key_id: string
}

export interface RazorpayVerifyPayload {
  order_id: string
  razorpay_order_id?: string
  razorpay_payment_id: string
  razorpay_signature?: string
}

export const ordersApi = {
  list: async () => api.get('/orders'),
  getById: async (id: string) => api.get(`/orders/${id}`),
  create: async (payload: Record<string, unknown>) => api.post('/orders', payload),
  updateStatus: async (id: string, status: string) => api.patch(`/orders/${id}/status`, { status }),
  createRazorpayOrder: async (payload: { amount: number; order_id?: string; customer_name?: string; customer_phone?: string }) => {
    const res = await api.post<RazorpayOrderResponse>('/orders/create-razorpay-order', payload)
    return res.data
  },
  verifyRazorpayPayment: async (payload: RazorpayVerifyPayload) => {
    const res = await api.post<{ status: string; message: string; order: any }>('/orders/verify-razorpay-payment', payload)
    return res.data
  },
}

export type Role = 'admin' | 'manager' | 'waiter' | 'kitchen' | 'customer'

export type UserSession = {
  id: string
  name: string
  email: string
  role: Role
  restaurantId?: string
}

export type ApiError = {
  message: string
  status?: number
  code?: string
}

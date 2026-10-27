export type SocketEvent = {
  type: string
  payload?: unknown
}

export class AppWebSocket {
  private socket: WebSocket | null = null
  private listeners = new Map<string, Set<(payload: unknown) => void>>()
  private url: string | null = null
  private shouldReconnect = false
  private reconnectAttempts = 0
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null

  connect(url: string) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN && this.url === url) {
      return
    }
    this.url = url
    this.shouldReconnect = true
    this.open()
  }

  private open() {
    if (!this.url) return
    try {
      this.socket = new WebSocket(this.url)
    } catch {
      this.scheduleReconnect()
      return
    }

    this.socket.onopen = () => {
      this.reconnectAttempts = 0
    }

    this.socket.onmessage = (event) => {
      let message: SocketEvent
      try {
        message = JSON.parse(event.data) as SocketEvent
      } catch {
        return // ignore malformed frames
      }
      const handlers = this.listeners.get(message.type) ?? []
      handlers.forEach((handler) => handler(message.payload))
    }

    this.socket.onerror = () => {
      this.socket?.close()
    }

    this.socket.onclose = () => {
      this.socket = null
      if (this.shouldReconnect) {
        this.scheduleReconnect()
      }
    }
  }

  private scheduleReconnect() {
    if (!this.shouldReconnect || this.reconnectTimer) return
    // Exponential backoff capped at 30s.
    const delay = Math.min(1000 * 2 ** this.reconnectAttempts, 30000)
    this.reconnectAttempts += 1
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null
      this.open()
    }, delay)
  }

  on(eventName: string, handler: (payload: unknown) => void) {
    const handlers = this.listeners.get(eventName) ?? new Set()
    handlers.add(handler)
    this.listeners.set(eventName, handlers)
  }

  off(eventName: string, handler: (payload: unknown) => void) {
    const handlers = this.listeners.get(eventName)
    if (!handlers) return
    handlers.delete(handler)
  }

  disconnect() {
    this.shouldReconnect = false
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    this.socket?.close()
    this.socket = null
  }
}

export const websocketClient = new AppWebSocket()

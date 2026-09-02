export type SocketEvent = {
  type: string
  payload?: unknown
}

export class AppWebSocket {
  private socket: WebSocket | null = null
  private listeners = new Map<string, Set<(payload: unknown) => void>>()

  connect(url: string) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return
    }

    this.socket = new WebSocket(url)

    this.socket.onmessage = (event) => {
      const message = JSON.parse(event.data) as SocketEvent
      const handlers = this.listeners.get(message.type) ?? []
      handlers.forEach((handler) => handler(message.payload))
    }
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
    this.socket?.close()
    this.socket = null
  }
}

export const websocketClient = new AppWebSocket()

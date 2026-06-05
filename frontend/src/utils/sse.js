export class SSEClient {
  constructor(url, options = {}) {
    this.url = url
    this.options = {
      headers: {},
      onMessage: () => {},
      onError: () => {},
      onOpen: () => {},
      ...options
    }
    this.eventSource = null
  }

  connect() {
    const eventSource = new EventSource(this.url, {
      headers: this.options.headers,
      withCredentials: true
    })

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        this.options.onMessage(data)
      } catch (e) {
        this.options.onMessage(event.data)
      }
    }

    eventSource.onerror = (error) => {
      this.options.onError(error)
      eventSource.close()
    }

    eventSource.onopen = () => {
      this.options.onOpen()
    }

    this.eventSource = eventSource
  }

  disconnect() {
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
    }
  }
}

export const createSSEStream = (url, handlers) => {
  const client = new SSEClient(url, handlers)
  client.connect()
  return client
}
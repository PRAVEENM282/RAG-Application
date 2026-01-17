export class WebSocketService {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.callbacks = {
            onToken: () => { },
            onCitation: () => { },
            onError: () => { },
            onDone: () => { },
        };
    }

    connect(token, callbacks) {
        this.callbacks = { ...this.callbacks, ...callbacks };
        this.ws = new WebSocket(`${this.url}?token=${token}`);

        this.ws.onopen = () => {
            console.log("Connected to WebSocket");
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            } catch (e) {
                console.error("Failed to parse websocket message", e);
            }
        };

        this.ws.onerror = (error) => {
            console.error("WebSocket error", error);
            if (this.callbacks.onError) this.callbacks.onError("Connection error");
        };

        this.ws.onclose = () => {
            console.log("WebSocket disconnected");
        };
    }

    sendMessage(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(message);
        } else {
            console.error("WebSocket is not connected");
            if (this.callbacks.onError) this.callbacks.onError("WebSocket not connected");
        }
    }

    handleMessage(data) {
        switch (data.type) {
            case "token":
                this.callbacks.onToken(data.payload);
                break;
            case "citation":
                this.callbacks.onCitation(data.payload);
                break;
            case "error":
                this.callbacks.onError(data.payload);
                break;
            case "done":
                this.callbacks.onDone();
                break;
            default:
                console.warn("Unknown message type", data.type);
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

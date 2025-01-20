class SignalingServer {
  constructor(wss) {
    this.wss = wss;
    this.connections = new Map();
    this.setupWSS();
  }

  setupWSS() {
    this.wss.on('connection', this.handleConnection.bind(this));
  }

  handleConnection(ws) {
    const connectionId = Date.now().toString();
    this.connections.set(connectionId, ws);

    ws.on('message', async (message) => {
      await this.handleMessage(ws, message);
    });

    ws.on('close', () => {
      this.connections.delete(connectionId);
    });

    ws.send(JSON.stringify({ 
      type: 'connected',
      id: connectionId 
    }));
  }

  async handleMessage(ws, message) {
    try {
      const data = JSON.parse(message);

      switch (data.type) {
        case 'offer':
          const answer = await this.createAnswer(data.offer);
          ws.send(JSON.stringify({
            type: 'answer',
            answer
          }));
          break;

        case 'answer':
          await this.handleAnswer(data.answer);
          break;

        case 'ice-candidate':
          await this.handleIceCandidate(data.candidate);
          break;

        default:
          throw new Error(`Unknown message type: ${data.type}`);
      }
    } catch (error) {
      ws.send(JSON.stringify({
        type: 'error',
        error: error.message
      }));
    }
  }

  async createAnswer(offer) {
    if (!offer || !offer.sdp || !offer.sdp.startsWith('v=0')) {
      throw new Error('Invalid SDP format');
    }

    const peerConnection = new RTCPeerConnection();
    await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);
    return answer;
  }

  async handleAnswer(answer) {
    if (!answer || !answer.sdp || !answer.sdp.startsWith('v=0')) {
      throw new Error('Invalid SDP format');
    }
  }

  async handleIceCandidate(candidate) {
    if (!candidate) {
      throw new Error('Invalid ICE candidate');
    }
  }
}

export default SignalingServer;
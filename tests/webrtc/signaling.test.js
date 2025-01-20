import SignalingServer from '../../src/webrtc/signaling';

describe('SignalingServer', () => {
  let server;
  let mockWSS;
  let ws;

  beforeEach(() => {
    // Setup WebSocket mock
    ws = {
      on: jest.fn((event, handler) => {
        if (!ws.listeners[event]) {
          ws.listeners[event] = [];
        }
        ws.listeners[event].push(handler);
        return ws;
      }),
      send: jest.fn(),
      listeners: {
        message: [],
        close: []
      }
    };

    // Setup WebSocket Server mock
    mockWSS = {
      on: jest.fn()
    };

    server = new SignalingServer(mockWSS);
    
    // Trigger the connection handler
    const connectionHandler = mockWSS.on.mock.calls[0][1];
    connectionHandler(ws);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should handle new connections', () => {
    expect(server.connections.size).toBe(1);
    expect(ws.on).toHaveBeenCalledWith('message', expect.any(Function));
    expect(ws.on).toHaveBeenCalledWith('close', expect.any(Function));
  });

  it('should handle offer messages', async () => {
    const mockOffer = {
      type: 'offer',
      offer: {
        type: 'offer',
        sdp: 'v=0\r\no=- 123456 2 IN IP4 127.0.0.1\r\n'
      }
    };

    // Clear initial connection message
    ws.send.mockClear();

    // Get message handler and call it
    const messageHandler = ws.listeners.message[0];
    await messageHandler(JSON.stringify(mockOffer));

    expect(ws.send).toHaveBeenCalledWith(
      expect.stringMatching(/"type":"answer"/)
    );
  });

  it('should handle invalid messages', async () => {
    const messageHandler = ws.listeners.message[0];
    await messageHandler('invalid json');
    
    expect(ws.send).toHaveBeenCalledWith(
      expect.stringMatching(/"type":"error"/)
    );
  });

  it('should clean up connections on close', () => {
    const closeHandler = ws.listeners.close[0];
    closeHandler();
    expect(server.connections.size).toBe(0);
  });
});
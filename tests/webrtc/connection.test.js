import WebRTCConnection from '../../src/webrtc/connection';

describe('WebRTCConnection', () => {
  let connection;

  beforeEach(() => {
    connection = new WebRTCConnection();
  });

  afterEach(() => {
    connection = null;
  });

  test('should create a connection instance', () => {
    expect(connection).toBeInstanceOf(WebRTCConnection);
  });

  test('should create an offer', async () => {
    const offer = await connection.createOffer();
    expect(offer).toHaveProperty('type', 'offer');
    expect(offer).toHaveProperty('sdp');
  });

  test('should handle ICE candidates', () => {
    const mockCandidate = { candidate: 'mock-candidate' };
    connection.onIceCandidate = jest.fn();
    connection.pc.onicecandidate({ candidate: mockCandidate });
    expect(connection.onIceCandidate).toHaveBeenCalledWith(mockCandidate);
  });

  test('should handle track events', () => {
    const mockTrack = { kind: 'audio' };
    connection.onTrack = jest.fn();
    connection.pc.ontrack({ track: mockTrack });
    expect(connection.onTrack).toHaveBeenCalledWith(mockTrack);
  });
});

// Global mocks and setup
global.console = {
  ...console,
  log: jest.fn(),
  error: jest.fn(),
  warn: jest.fn()
};

// Mock WebRTC globals
global.RTCPeerConnection = jest.fn().mockImplementation(() => ({
  createOffer: jest.fn(),
  createAnswer: jest.fn(),
  setLocalDescription: jest.fn(),
  setRemoteDescription: jest.fn(),
  addIceCandidate: jest.fn(),
  addTrack: jest.fn(),
  close: jest.fn()
}));

global.RTCSessionDescription = jest.fn();
global.RTCIceCandidate = jest.fn();

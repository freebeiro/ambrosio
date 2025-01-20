require('@jest/globals');

Object.assign(global, {
  window: {
    AudioContext: jest.fn().mockImplementation(() => ({
      createMediaStreamSource: jest.fn().mockReturnValue({
        connect: jest.fn()
      }),
      createAnalyser: jest.fn().mockReturnValue({
        connect: jest.fn(),
        frequencyBinCount: 1024,
        getByteFrequencyData: jest.fn()
      }),
      close: jest.fn().mockResolvedValue(undefined),
      destination: {}
    })),
    webkitAudioContext: undefined
  },
  
  navigator: {
    mediaDevices: {
      getUserMedia: jest.fn()
    }
  },
  
  RTCPeerConnection: jest.fn().mockImplementation(() => ({
    setRemoteDescription: jest.fn().mockResolvedValue(undefined),
    createAnswer: jest.fn().mockResolvedValue({ type: 'answer', sdp: 'v=0\r\n' }),
    setLocalDescription: jest.fn().mockResolvedValue(undefined)
  }))
});
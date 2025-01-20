import AudioProcessor from '../../src/webrtc/audio';

describe('AudioProcessor', () => {
  let audioProcessor;
  let mockConnection;
  let mockTrack;
  let mockStream;
  let mockAudioContext;

  beforeEach(() => {
    // Create mock track and stream
    mockTrack = { stop: jest.fn() };
    mockStream = {
      getAudioTracks: jest.fn().mockReturnValue([mockTrack]),
      getTracks: jest.fn().mockReturnValue([mockTrack])
    };

    // Create mock audio context
    mockAudioContext = {
      createMediaStreamSource: jest.fn().mockReturnValue({
        connect: jest.fn()
      }),
      createAnalyser: jest.fn().mockReturnValue({
        connect: jest.fn(),
        frequencyBinCount: 1024,
        getByteFrequencyData: jest.fn(arr => arr.fill(128))
      }),
      close: jest.fn().mockResolvedValue(undefined),
      destination: {}
    };

    // Create proper constructor mocks
    const AudioContextMock = jest.fn(() => mockAudioContext);
    const WebkitAudioContextMock = jest.fn(() => mockAudioContext);
    
    // Setup global mocks
    global.window = {
      AudioContext: AudioContextMock,
      webkitAudioContext: WebkitAudioContextMock
    };
    global.navigator = {
      mediaDevices: {
        getUserMedia: jest.fn().mockResolvedValue(mockStream)
      }
    };

    // Create mock connection and processor
    mockConnection = {
      addTrack: jest.fn()
    };
    audioProcessor = new AudioProcessor();
  });

  afterEach(async () => {
    jest.clearAllMocks();
    if (audioProcessor.initialized) {
      await audioProcessor.cleanup();
    }
    delete global.window;
    delete global.navigator;
  });

  it('should initialize audio processing', async () => {
    const result = await audioProcessor.initialize(mockConnection);
    expect(result).toBe(true);
    expect(audioProcessor.initialized).toBe(true);
    expect(mockConnection.addTrack).toHaveBeenCalledWith(mockTrack, mockStream);
  });

  it('should handle audio initialization errors', async () => {
    const mockError = new Error('Audio failed');
    global.navigator.mediaDevices.getUserMedia.mockRejectedValueOnce(mockError);
    
    await expect(audioProcessor.initialize(mockConnection))
      .rejects.toThrow('Audio failed');
    
    expect(audioProcessor.initialized).toBe(false);
  });

  it('should monitor audio levels', async () => {
    await audioProcessor.initialize(mockConnection);
    const level = audioProcessor.getAudioLevel();
    expect(level).toBeCloseTo(0.5, 2); // 128/255 ≈ 0.5 with 2 decimal precision
  });

  it('should clean up resources', async () => {
    await audioProcessor.initialize(mockConnection);
    await audioProcessor.cleanup();
    
    expect(mockTrack.stop).toHaveBeenCalled();
    expect(audioProcessor.audioContext).toBeNull();
    expect(audioProcessor.initialized).toBe(false);
  });
});

class AudioProcessor {
  constructor() {
    this.reset();
  }

  reset() {
    this.audioContext = null;
    this.audioStream = null;
    this.audioSource = null;
    this.analyser = null;
    this.initialized = false;
  }

  async initialize(connection) {
    if (this.initialized) {
      return true;
    }

    try {
      // Create audio context first
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      
      // Get user media
      this.audioStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      });

      if (!this.audioStream) {
        throw new Error('Failed to get audio stream');
      }

      // Setup audio processing
      this.audioSource = this.audioContext.createMediaStreamSource(this.audioStream);
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 2048;
      
      // Connect nodes
      this.audioSource.connect(this.analyser);
      this.analyser.connect(this.audioContext.destination);

      // Add track to connection
      const audioTrack = this.audioStream.getAudioTracks()[0];
      if (audioTrack) {
        connection.addTrack(audioTrack, this.audioStream);
      }

      this.initialized = true;
      return true;

    } catch (error) {
      this.reset();
      throw error;
    }
  }

  async cleanup() {
    if (this.audioStream) {
      this.audioStream.getTracks().forEach(track => track.stop());
    }
    
    if (this.audioContext) {
      try {
        await this.audioContext.close();
      } catch (error) {
        console.error('Error closing audio context:', error);
      }
    }

    this.reset();
  }

  getAudioLevel() {
    if (!this.initialized || !this.analyser) {
      return 0;
    }

    const dataArray = new Uint8Array(this.analyser.frequencyBinCount);
    this.analyser.getByteFrequencyData(dataArray);

    // Calculate average volume level
    const sum = dataArray.reduce((acc, val) => acc + val, 0);
    return sum / (dataArray.length * 255); // Normalize to 0-1
  }
}

export default AudioProcessor;
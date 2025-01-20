import { RTCPeerConnection } from '@roamhq/wrtc';
import config from './webrtc.config.json';

class WebRTCConnection {
  constructor() {
    this.pc = new RTCPeerConnection(config);
    this.setupEventHandlers();
  }

  setupEventHandlers() {
    this.pc.onicecandidate = (event) => {
      if (event.candidate) {
        this.onIceCandidate(event.candidate);
      }
    };

    this.pc.oniceconnectionstatechange = () => {
      this.onIceConnectionStateChange(this.pc.iceConnectionState);
    };

    this.pc.ontrack = (event) => {
      this.onTrack(event.track);
    };
  }

  async createOffer() {
    const offer = await this.pc.createOffer({
      offerToReceiveAudio: true,
      offerToReceiveVideo: false
    });
    await this.pc.setLocalDescription(offer);
    return offer;
  }

  async setRemoteDescription(description) {
    await this.pc.setRemoteDescription(description);
  }

  async addIceCandidate(candidate) {
    await this.pc.addIceCandidate(candidate);
  }

  onIceCandidate(candidate) {
    // Implement candidate handling
  }

  onIceConnectionStateChange(state) {
    // Implement state change handling
  }

  onTrack(track) {
    // Implement track handling
  }
}

export default WebRTCConnection;

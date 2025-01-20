# OpenAI Realtime API Integration for Ambrosio

This document outlines how we'll implement OpenAI's Realtime API features in the Ambrosio project.

## Key Features to Implement

1. **WebRTC Connection**
   - Use ephemeral API keys for secure client connections
   - Implement WebRTC peer connection for low-latency audio
   - Configure audio input/output streams

2. **Wake Word Detection**
   - Integrate Picovoice Porcupine for "Ambrosio" wake word
   - Combine with OpenAI's voice activity detection
   - Implement push-to-talk fallback

3. **Home Assistant Integration**
   - Use function calling to interact with Home Assistant API
   - Implement device control commands
   - Add error handling for device states

4. **Audio Processing**
   - Configure audio formats for European Portuguese
   - Implement real-time transcription
   - Handle audio stream interruptions

## Implementation Steps

### 1. WebRTC Setup
- Create WebRTC peer connection
- Configure audio input/output streams
- Implement session management

### 2. Wake Word Integration
- Initialize Picovoice Porcupine
- Configure wake word sensitivity
- Implement wake word state management

### 3. Home Assistant Function Calls
- Define Home Assistant API functions
- Implement device control logic
- Add error handling for API calls

### 4. Audio Configuration
- Set up audio codecs for European Portuguese
- Implement real-time transcription
- Configure audio stream buffers

## Example Code Structure

```javascript
// WebRTC Connection
const pc = new RTCPeerConnection();

// Audio Setup
const audioEl = document.createElement("audio");
audioEl.autoplay = true;
pc.ontrack = e => audioEl.srcObject = e.streams[0];

// Home Assistant Function
const homeAssistantFunctions = [
  {
    name: "control_device",
    description: "Control smart home devices",
    parameters: {
      type: "object",
      properties: {
        device: { type: "string" },
        action: { type: "string", enum: ["on", "off"] }
      }
    }
  }
];

// Session Configuration
const sessionConfig = {
  model: "gpt-4o-realtime-preview-2024-12-17",
  voice: "portuguese",
  tools: homeAssistantFunctions
};
```

## Next Steps

1. Implement WebRTC connection handler
2. Configure Picovoice wake word detection
3. Develop Home Assistant API integration
4. Set up audio processing pipeline

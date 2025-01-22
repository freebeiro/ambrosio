# Ambrosio Development Guidelines

## Development Standards
### SOLID Principles
- **Single Responsibility**: Each component handles one specific task
- **Open/Closed**: Extend functionality through new integrations
- **Liskov Substitution**: Components implement clear interfaces
- **Interface Segregation**: Focused, minimal interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

### Error Handling
- Retry transient errors (e.g., OpenAI API calls)
- Validate all inputs (e.g., Home Assistant entity IDs)
- Log errors with context using ProductionLogger
- Implement circuit breakers for external services

### Logging Implementation
- Uses dependency injection through ILogger interface
- ProductionLogger provides:
  - Info: System status and normal operations
  - Debug: Detailed technical information
  - Error: Critical failures and exceptions
- Configurable log levels and file rotation

## Testing Requirements
### Core Functionality
- **Wake Word Detection**:
  - Test with 10+ voice samples
  - Validate different noise levels
  - Measure detection latency (<500ms)

- **Audio I/O**:
  - Validate on macOS and Raspberry Pi
  - Test microphone/speaker compatibility
  - Verify audio quality metrics

- **Home Assistant Integration**:
  - Ensure command execution within 500ms
  - Validate entity discovery
  - Maintain 100% success rate for valid commands

## Documentation
- Add inline comments for complex logic
- Document new voice provider integration process
- Maintain API reference documentation
- Keep architecture diagrams updated
- Use consistent Markdown formatting

## Implementation Checklist
- [ ] Verify .env configuration matches template
- [ ] Test core components individually:
  ```bash
  # Test wake word detection
  python3 -c "from integrations.wake_word.porcupine import PorcupineWakeWordDetector; detector = PorcupineWakeWordDetector('dummy_key', 'dummy.ppn')"
  
  # Test OpenAI integration
  python3 -c "from integrations.voice_processing.openai_realtime import OpenAIVoiceProcessor; processor = OpenAIVoiceProcessor('dummy_key', 'dummy_prompt')"
  ```
- [ ] Validate integration points
- [ ] Confirm logging works across all components
- [ ] Ensure error handling covers all scenarios

## Deliverables
- Fully functional Python implementation
- Validation report containing:
  - Wake word detection accuracy metrics
  - OpenAI response latency measurements
  - Home Assistant command success rates
  - Audio I/O performance statistics

# Why Markdown?
1. **Readability**: Clear structure with headings and lists  
2. **Portability**: Viewable in any editor or browser  
3. **Maintainability**: Easy to update and version control  
4. **AI Compatibility**: Optimal format for LLM processing

# Usage Instructions
1. Save this document as `GUIDELINES.md`
2. Follow the implementation checklist rigorously
3. Refer to testing requirements before deployment
4. Update documentation with any changes

Guidelines
SOLID Compliance
Single Responsibility: No component handles more than one task.

Open/Closed: New tools are added via /integrations without modifying existing code.

Dependency Inversion: All components depend on interfaces, not concrete classes.

Error Handling
Retry transient errors (e.g., OpenAI API calls).

Validate all inputs (e.g., Home Assistant entity IDs).

Log errors with context using ProductionLogger.

Testing
Wake Word Detection: Test with 10+ voice samples.

Audio I/O: Validate on macOS and Raspberry Pi.

Home Assistant: Ensure commands execute within 500ms.

Documentation
Add inline comments explaining complex logic.

Document how to add new voice providers in /integrations.

Deliverables
Fully functional Python implementation matching the provided structure.

Validation report confirming:

Wake word detection accuracy.

OpenAI response latency (<1.5s).

Home Assistant command success rate (100% for valid commands).

Instructions for AI Worker
Implement Exactly As Provided:

Copy all code files verbatim.

Maintain directory structure.

Validate Configuration:

Ensure .env matches the template.

Test with python3 -c "from config.settings import Settings; Settings()".

Test Components Individually:

bash
Copy
# Test wake word detection
python3 -c "from integrations.wake_word.porcupine import PorcupineWakeWordDetector; detector = PorcupineWakeWordDetector('dummy_key', 'dummy.ppn')"

# Test OpenAI integration
python3 -c "from integrations.voice_processing.openai_realtime import OpenAIVoiceProcessor; processor = OpenAIVoiceProcessor('dummy_key', 'dummy_prompt')"
Reply with "ACKNOWLEDGED" to confirm understanding, then begin implementation.
Ask for clarification if any part of the code/instructions is unclear.

Copy

---

### **Why Markdown?**
1. **Readability**: Clear headings, code blocks, and lists make it easy to follow.  
2. **Portability**: Can be viewed in any text editor or rendered in tools like GitHub.  
3. **AI-Friendly**: Most AI tools parse Markdown effectively.  

---

### **How to Use**
1. Save the above content as `ambrosio_implementation.md`.  
2. Provide the file to the AI worker with the following instructions:  
   ```text
   Read the instructions in `ambrosio_implementation.md` carefully.  
   Implement the project exactly as described.  
   Ask for clarification if anything is unclear.  
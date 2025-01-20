Porcupine Wake Word
Porcupine is a highly-accurate and lightweight wake word engine. It enables building always-listening voice-enabled applications. It is

using deep neural networks trained in real-world environments.
compact and computationally-efficient. It is perfect for IoT.
cross-platform:
Arm Cortex-M, STM32, Arduino, and i.MX RT
Raspberry Pi (Zero, 3, 4, 5)
Android and iOS
Chrome, Safari, Firefox, and Edge
Linux (x86_64), macOS (x86_64, arm64), and Windows (x86_64)
scalable. It can detect multiple always-listening voice commands with no added runtime footprint.
self-service. Developers can train custom wake word models using Picovoice Console.
Arabic
اَلْعَرَبِيَّةُ
Dutch
Nederlands
English
English
Farsi
فارسی
French
Français
German
Deutsch
Hindi
हिन्दी
Italian
Italiano
Japanese
日本語
Korean
한국어
Mandarin
普通话
Polish
Polski
Portuguese
Português
Russian
Русский
Spanish
Español
Swedish
Svenska
Vietnamese
Tiếng Việt
Afrikaans
Afrikaans
Bengali
বাংলা
Bulgarian
български
Croatian
Hrvatski
Czech
Čeština
Danish
Dansk
Estonian
Eesti keel
Finnish
Suomi
Greek
Ελληνικά
Hebrew
עִברִית
Hungarian
Magyar
Icelandic
Íslenska
Indonesian
Bahasa Indonesia
Irish
Gaeilge
Norwegian
Norsk Bokmål
Romanian
Daco-Romanian
Serbian
Cрпски језик
Slovak
Slovenčina
Slovenian
Slovenski jezik
Thai
ภาษาไทย
Turkish
Türkçe
Ukrainian
Yкраїнська мова
Urdu
اردو
Get Started
Anyone who is using Picovoice needs to have a valid AccessKey. AccessKey is your authentication and authorization token for using Picovoice. It also verifies that your usage is within the limits of your account. You must keep your AccessKey secret!

Sign up for Picovoice Console
Sign up for Picovoice Console. It is free, no credit card required.

Obtain your AccessKey
Log in to your Picovoice Console account and copy your AccessKey from the home page:

Download SDK
Picovoice SDKs are available both on GitHub and via SDK-specific package managers. Follow one of the quick starts to get started with Porcupine using your newly-created AccessKey.

Android
Angular
Arduino
C
Chrome
.NET
Edge
Firefox
Flutter
Go
iOS
Java
Linux
macOS
Microcontroller
Node.js
Python
Raspberry Pi
React
React Native
Rust
Safari
Unity
Vue
Web
Windows
Custom Wake Words
Log in to the Picovoice Console and navigate to the Porcupine page.

Create your Wake Word
A unique feature of the Porcupine wake word engine is that one can simply type in the trigger phrase and it will train a model for that specific phrase within seconds. Picovoice uses a technique called transfer learning, which mimics how humans learn new phrases.

When in the wake word console, select a language and type the wake phrase you want to train:

The choice of phrase is important for both accuracy and user experience. A good wake phrase needs to have some properties in terms of length and number of syllables. See Tips for Choosing a Wake Word for a summary.

The Console will validate your wake phrase and let you know if it's a good choice.

Test
Once you have entered a valid wake word, you can test it right in your browser. Test the wake phrase using the microphone button:

Even if you turn off your WiFi, the testing will continue to function, as all voice processing is performed in the browser itself.

Train
Click on the Train button and select which platform you'd like the model to be trained for:

The wake word models created by Console are platform-specific: a model trained for Raspberry Pi cannot run on Android, for example.

Once you've selected a valid platform, click the Download button to initiate training and download the result.

The model file (.ppn) will train in seconds and start downloading immediately upon a successful training.

Use the .ppn file with the Picovoice SDK or Porcupine directly as a wake word / always-listening component of your voice user interface.


Porcupine Wake Word
Node.js Quick Start
Platforms
Linux (x86_64)
macOS (x86_64, arm64)
Windows (x86_64)
Raspberry Pi (3, 4, 5)
Looking to run Porcupine Wake Word in-browser?
Requirements
Picovoice Account & AccessKey
Node.js 16+
npm
Picovoice Account & AccessKey
Signup or Login to Picovoice Console to get your AccessKey. Make sure to keep your AccessKey secret.

Quick Start
Setup
Install Node.js .

Install the porcupine-node  npm package:

npm install @picovoice/porcupine-node
Usage
Create an instance of Porcupine that detects the included built-in wake words porcupine and bumblebee with sensitivities of 0.5 and 0.65, respectively.

const {
  Porcupine,
  BuiltinKeyword,
}= require("@picovoice/porcupine-node");

const accessKey = "${ACCESS_KEY}"
let porcupine = new Porcupine(
    accessKey,
    [BuiltinKeyword.GRASSHOPPER, BuiltinKeyword.BUMBLEBEE],
    [0.5, 0.65]
);
Pass in frames of audio to the .process function:

function getNextAudioFrame() {
  // ...
  return audioFrame;
}

while (true) {
  const audioFrame = getNextAudioFrame();
  const keywordIndex = porcupine.process(audioFrame);
  if (keywordIndex === 0) {
    // detected `porcupine
  } else if (keywordIndex === 1) {
    // detected `bumblebee`
  }
}
Release resources explicitly when done with Porcupine:

porcupine.release()
Custom Keywords
Create custom keywords using the Picovoice Console. Download the custom wake word file (.ppn) and create an instance of Porcupine Wake Word by passing in the path to the keyword file.

const porcupine = new Porcupine(
  '${ACCESS_KEY}',
  ['${KEYWORD_FILE_PATH}'],
  [0.5]
);
Non-English Languages
Use the corresponding model file (.pv) to detect non-English wake words. The model files for all supported languages are available on the Porcupine Wake Word GitHub repository .

Pass in the model file to change the detection language:

const porcupine = new Porcupine(
  '${ACCESS_KEY}',
  ['${KEYWORD_FILE_PATH}'],
  [0.5],
  '${MODEL_FILE_PATH}'
);
Demo
For the Porcupine Wake Word Node.js SDK, we offer demo applications that demonstrate how to use the Wake Word engine on real-time audio streams (i.e. microphone input) and audio files.

Setup
Install the Porcupine Wake Word demo package :

npm install -g @picovoice/porcupine-node-demo
This package installs command-line utilities for the Porcupine Wake Word Node.js demos.

Usage
Use the --help flag to see the usage options for the demo:

ppn-mic-demo --help
Ensure you have a working microphone connected to your system and run the following command to detect the built-in keyword porcupine:

Copy
ppn-mic-demo \
--access_key ${ACCESS_KEY} \
--keywords porcupine \


Porcupine Wake Word
Node.js API
API Reference for the Node.js Porcupine SDK  (npmjs ).

Porcupine 
class Porcupine
Class for the Porcupine wake word engine. Porcupine can be initialized using the class constructor(). Resources should be cleaned when you are done using the release() method.

Porcupine.constructor() 
Porcupine.constructor(
  accessKey,
  keywords,
  sensitivities,
  manualModelPath,
  manualLibraryPath
)
constructor method for Porcupine wake word engine.

Parameters

accessKey string : AccessKey obtained from Picovoice Console.
keywords Array<string> : Absolute paths to keyword model files.
sensitivities Array<number> : Sensitivities for detecting keywords. Each value should be a number within [0, 1]. A higher sensitivity results in fewer misses at the cost of increasing the false alarm rate.
manualModelPath string : Absolute path to the file containing model parameters.
manualLibraryPath string : Absolute path to Porcupine's dynamic library.
Returns

Porcupine: An instance of Porcupine wake word engine.
Porcupine.process() 
Porcupine.process(frame)
Processes a frame of the incoming audio stream and emits the detection result. The number of samples per frame can be attained by calling .frameLength. The incoming audio needs to have a sample rate equal to .sampleRate and be 16-bit linearly-encoded. Porcupine operates on single-channel audio.

Parameters

frame Array<number> : A frame of audio samples.
Returns

number : Index of observed keyword at the end of the current frame. Indexing is 0-based and matches the ordering of keyword models provided to the constructor. If no keyword is detected then it returns -1.
Porcupine.frameLength 
Porcupine.frameLength
The number of audio samples per frame.

Porcupine.sampleRate 
Porcupine.sampleRate
The audio sample rate accepted by the Porcupine engine.

Porcupine.version 
Porcupine.version
The version of the Porcupine engine.

Porcupine.release() 
Porcupine.release()
Releases resources acquired by Porcupine

Errors 
Exceptions thrown if an error occurs within Porcupine Wake Word engine.

Exceptions:

Copy
class PvStatusOutOfMemoryError        extends Error {}
class PvStatusIoError                 extends Error {}
class PvStatusInvalidArgumentError    extends Error {}
class PvStatusStopIterationError      extends Error {}
class PvStatusKeyError                extends Error {}
class PvStatusInvalidStateError       extends Error {}
class PvStatusRuntimeError            extends Error {}
class PvStatusActivationError         extends Error {}
class PvStatusActivationLimitReached  extends Error {}
class PvStatusActivationThrottled     extends Error {}
class PvStatusActivationRefused       extends Error {}
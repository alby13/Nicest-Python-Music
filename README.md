Greetings Python lovers and music lovers. Using the latest Artificial Intelligence of the end of 2025, I have put together three code examples that generate music using only Python code.

I present three different code version because the "best sounding" song is subjective, so these are the best ones that I could create.

# Music_1.py

- Multiple harmonics (fundamental + 2nd, 3rd, 4th overtones) for rich piano-like timbre

- ADSR envelope (Attack-Decay-Sustain-Release) for natural note shaping

- "Für Elise" melody - the famous Beethoven piece opening

- The song is fully generated and saved. You can download beautiful_song.wav

# Music_2.py

Brief summary:
It generates a short (20-second) beautiful ambient/atmospheric piece in C major entirely from scratch using pure Python + NumPy/SciPy:

- Creates basic sine-wave tones at musical pitch frequencies (from a NOTES dictionary).
- Combines multiple tones into chords.
- Applies an ADSR envelope to each sound so notes fade in/out naturally instead of being harsh.
- Adds a simple reverb effect (delayed echo).
- Plays a slow 4-chord progression (I–V–vi–IV: C → G → Am → F) with sustained, reverberated chords in the low-mid range.
- Layers a gentle, higher-register melody on top (8 notes that softly arpeggiate over the chords).
- Mixes chords + melody, normalizes the audio, converts to 16-bit WAV, saves it as generated_music.wav, and tries to play it automatically depending on your OS (macOS/Windows/Linux).

Result: A calm, dreamy, pad-like ambient track with reverb — no external samples or instruments, just math → sound.

# Music_3.py

An even higher quality approach than Music_2 with more advanced synthesis, using harmonics and better sound design.

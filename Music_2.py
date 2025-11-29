import numpy as np
from scipy.io import wavfile
import os
import platform

# Music generation functions
def generate_tone(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a pure tone"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def apply_envelope(wave, attack=0.1, decay=0.1, sustain=0.7, release=0.2):
    """Apply ADSR envelope for more natural sound"""
    length = len(wave)
    attack_samples = int(attack * length)
    decay_samples = int(decay * length)
    release_samples = int(release * length)
    sustain_samples = length - attack_samples - decay_samples - release_samples
    
    envelope = np.concatenate([
        np.linspace(0, 1, attack_samples),
        np.linspace(1, sustain, decay_samples),
        np.ones(sustain_samples) * sustain,
        np.linspace(sustain, 0, release_samples)
    ])
    
    return wave * envelope

def generate_chord(frequencies, duration, sample_rate=44100):
    """Generate a chord from multiple frequencies"""
    waves = [generate_tone(f, duration, sample_rate) for f in frequencies]
    chord = np.sum(waves, axis=0) / len(frequencies)
    return apply_envelope(chord)

def add_reverb(wave, sample_rate=44100, delay=0.1, decay=0.3):
    """Add simple reverb effect"""
    delay_samples = int(delay * sample_rate)
    reverb = np.zeros(len(wave) + delay_samples)
    reverb[:len(wave)] += wave
    reverb[delay_samples:] += wave * decay
    return reverb[:len(wave)]

# Musical scales and progressions
NOTES = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
    'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
    'C3': 130.81, 'E3': 164.81, 'G3': 196.00, 'A3': 220.00
}

def create_ambient_music(duration=20, sample_rate=44100):
    """Create beautiful ambient/atmospheric music"""
    
    # Chord progression (I-V-vi-IV in C major)
    progressions = [
        [NOTES['C3'], NOTES['E3'], NOTES['G3']],  # C major
        [NOTES['G3'], NOTES['B4'], NOTES['D4']],   # G major
        [NOTES['A3'], NOTES['C4'], NOTES['E4']],   # A minor
        [NOTES['F4'], NOTES['A4'], NOTES['C5']]    # F major
    ]
    
    melody_notes = ['E5', 'D5', 'C5', 'D5', 'E5', 'G5', 'F5', 'E5']
    
    music = np.array([])
    chord_duration = duration / len(progressions)
    note_duration = chord_duration / len(melody_notes)
    
    for i, chord_freqs in enumerate(progressions):
        # Generate sustained chord
        chord = generate_chord(chord_freqs, chord_duration, sample_rate)
        chord = add_reverb(chord, sample_rate) * 0.4
        
        # Generate melody
        melody = np.zeros(int(chord_duration * sample_rate))
        for j, note in enumerate(melody_notes):
            start = int(j * note_duration * sample_rate)
            note_wave = generate_tone(NOTES[note], note_duration * 0.8, sample_rate, 0.2)
            note_wave = apply_envelope(note_wave, attack=0.05, release=0.3)
            end = start + len(note_wave)
            melody[start:end] += note_wave
        
        # Combine chord and melody
        combined = chord + melody
        music = np.concatenate([music, combined])
    
    # Normalize
    music = music / np.max(np.abs(music)) * 0.8
    return music.astype(np.float32)

def play_audio(filename):
    """Play audio file cross-platform"""
    system = platform.system()
    
    try:
        if system == 'Darwin':  # macOS
            os.system(f'afplay "{filename}"')
        elif system == 'Windows':
            os.system(f'start "" "{filename}"')
        elif system == 'Linux':
            os.system(f'aplay "{filename}"')
        else:
            print(f"Audio file saved to: {filename}")
            print("Please play it manually.")
    except Exception as e:
        print(f"Could not auto-play. File saved to: {filename}")
        print(f"Error: {e}")

# Generate and save the music
print("Generating beautiful ambient music...")
sample_rate = 44100
music = create_ambient_music(duration=20, sample_rate=sample_rate)

# Convert to 16-bit PCM
music_int = np.int16(music * 32767)

# Save to file
filename = "generated_music.wav"
wavfile.write(filename, sample_rate, music_int)
print(f"Music generated and saved to: {filename}")

# Play the music
print("Playing music...")
play_audio(filename)

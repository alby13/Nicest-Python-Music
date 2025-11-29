import numpy as np
from scipy.io import wavfile
import os
import platform

def generate_harmonic_tone(fundamental, duration, sample_rate=44100, harmonics=5):
    """Generate a tone with harmonics for richer sound"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.zeros_like(t)
    
    # Add fundamental and harmonics
    for i in range(1, harmonics + 1):
        amplitude = 0.3 / i  # Decrease amplitude for higher harmonics
        wave += amplitude * np.sin(2 * np.pi * fundamental * i * t)
    
    return wave

def generate_pad_sound(frequencies, duration, sample_rate=44100):
    """Generate warm pad sound with detuning"""
    waves = []
    for freq in frequencies:
        # Create slightly detuned versions for chorus effect
        for detune in [-2, 0, 2]:
            wave = generate_harmonic_tone(freq + detune, duration, sample_rate, harmonics=4)
            waves.append(wave)
    
    pad = np.sum(waves, axis=0) / len(waves)
    
    # Apply slow attack and release
    envelope = np.concatenate([
        np.linspace(0, 1, int(0.3 * sample_rate)),  # Slow attack
        np.ones(int((duration - 0.6) * sample_rate)),
        np.linspace(1, 0, int(0.3 * sample_rate))   # Slow release
    ])[:len(pad)]
    
    return pad * envelope * 0.5

def create_professional_music(duration=25, sample_rate=44100):
    """Create professional-sounding generative music"""
    
    # Beautiful chord progression
    progressions = [
        [261.63, 329.63, 392.00],  # C major
        [293.66, 369.99, 440.00],  # D minor
        [220.00, 277.18, 329.63],  # A minor
        [349.23, 440.00, 523.25],  # F major
        [392.00, 493.88, 587.33],  # G major
    ]
    
    music = np.array([])
    chord_duration = duration / len(progressions)
    
    for chord in progressions:
        pad = generate_pad_sound(chord, chord_duration, sample_rate)
        music = np.concatenate([music, pad])
    
    # Add subtle bass line
    bass_notes = [130.81, 146.83, 110.00, 174.61, 196.00]
    bass = np.array([])
    for note in bass_notes:
        bass_tone = generate_harmonic_tone(note, chord_duration, sample_rate, harmonics=2)
        bass_tone = bass_tone * 0.3
        bass = np.concatenate([bass, bass_tone])
    
    # Mix everything
    music = music[:len(bass)] + bass[:len(music)]
    
    # Normalize
    music = music / np.max(np.abs(music)) * 0.85
    return music.astype(np.float32)

# Generate high-quality music
print("🎵 Generating high-quality music...")
sample_rate = 44100
music = create_professional_music(duration=25, sample_rate=sample_rate)

# Save
music_int = np.int16(music * 32767)
filename = "beautiful_music.wav"
wavfile.write(filename, sample_rate, music_int)
print(f"✓ Music saved to: {filename}")

# Auto-play
print("▶ Playing...")
system = platform.system()
if system == 'Darwin':
    os.system(f'afplay "{filename}"')
elif system == 'Windows':
    os.system(f'start "" "{filename}"')
else:
    os.system(f'aplay "{filename}" 2>/dev/null || echo "Play {filename} manually"')

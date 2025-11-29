import time
import math
import wave
import struct

# Create high-quality song with harmonics and ADSR envelope
def create_beautiful_song(filename="beautiful_song.wav", sample_rate=44100):
    """
    Create a beautiful melody with proper synthesis
    """
    notes = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'REST': 0
    }
    
    # "Für Elise" opening
    melody = [
        ('E5', 0.3), ('D5', 0.3), ('E5', 0.3), ('D5', 0.3), ('E5', 0.3),
        ('B4', 0.3), ('D5', 0.3), ('C5', 0.3), ('A4', 0.6),
        ('REST', 0.3), ('C4', 0.3), ('E4', 0.3), ('A4', 0.3), ('B4', 0.6),
        ('REST', 0.3), ('E4', 0.3), ('G4', 0.3), ('B4', 0.3), ('C5', 0.6),
    ]
    
    audio_data = []
    
    for note_name, duration in melody:
        if note_name == 'REST':
            num_samples = int(sample_rate * duration)
            for i in range(num_samples):
                audio_data.append(0)
        else:
            frequency = notes[note_name]
            num_samples = int(sample_rate * duration)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                
                # ADSR Envelope
                attack_time = 0.01
                decay_time = 0.05
                release_time = 0.1
                
                attack_samples = int(sample_rate * attack_time)
                decay_samples = int(sample_rate * decay_time)
                release_samples = int(sample_rate * release_time)
                
                if i < attack_samples:
                    envelope = i / attack_samples
                elif i < attack_samples + decay_samples:
                    envelope = 1.0 - 0.3 * (i - attack_samples) / decay_samples
                elif i > num_samples - release_samples:
                    envelope = 0.7 * (num_samples - i) / release_samples
                else:
                    envelope = 0.7
                
                # Add harmonics for richer piano-like sound
                fundamental = math.sin(2 * math.pi * frequency * t)
                harmonic2 = 0.3 * math.sin(2 * math.pi * frequency * 2 * t)
                harmonic3 = 0.15 * math.sin(2 * math.pi * frequency * 3 * t)
                harmonic4 = 0.08 * math.sin(2 * math.pi * frequency * 4 * t)
                
                wave_value = fundamental + harmonic2 + harmonic3 + harmonic4
                sample = int(32767 * 0.25 * envelope * wave_value)
                audio_data.append(sample)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, len(audio_data), 'NONE', 'not compressed'))
        for sample in audio_data:
            wav_file.writeframes(struct.pack('h', sample))
    
    print(f"✓ Song created: {filename}")
    return filename

# Create the song
song_file = create_beautiful_song()

# Now play it directly using pygame
print("\n🎵 Installing and playing with pygame...")

try:
    import subprocess
    import sys
    
    # Try to install pygame
    print("Installing pygame...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pygame"])
    print("✓ pygame installed!")
    
    # Import and play
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load(song_file)
    
    print("\n🎵 NOW PLAYING: Für Elise (opening)")
    print("="*50)
    pygame.mixer.music.play()
    
    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    print("="*50)
    print("✓ Playback complete!")
    
except Exception as e:
    print(f"Note: Could not auto-install/play. Error: {e}")
    print(f"\nYour song file '{song_file}' is ready!")
    print("Download it and play with any audio player.")

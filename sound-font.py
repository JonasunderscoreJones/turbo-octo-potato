from pydub import AudioSegment
import fluidsynth
import os

# Load the MP3 file
input_file = "/home/jonas_jones/Downloads/apple-crunch.mp3"
audio = AudioSegment.from_mp3(input_file)

# Define the piano pitch range (from C1 to C7)
piano_keys = 88  # 88 keys on a piano
pitch_range = list(range(1, piano_keys + 1))

# Create a temporary directory to store individual pitch-shifted audio files
temp_dir = "temp_audio"
os.makedirs(temp_dir, exist_ok=True)

# Export and pitch-shift the audio in different pitches
for pitch in pitch_range:
    # Calculate the ratio for pitch shift (12 semitones = 1 octave)
    semitone_ratio = 2 ** (pitch / 12.0)
    # Shift the pitch
    shifted_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * semitone_ratio)
    })
    # Export the shifted audio
    output_file = os.path.join(temp_dir, f"output_pitch_{pitch}.wav")
    shifted_audio.export(output_file, format="wav")

print("Audio exported in different pitches.")

# Create an empty SoundFont
soundfont = fluidsynth.SoundFont()

# Load the pitch-shifted audio files into the SoundFont
for pitch in pitch_range:
    audio_file = os.path.join(temp_dir, f"output_pitch_{pitch}.wav")
    soundfont.add_sample(audio_file, preset=0, note=pitch)

# Save the SoundFont to a file
soundfont_file = "output_soundfont.sf2"
soundfont.write_to_file(soundfont_file)

print(f"SoundFont '{soundfont_file}' created.")

# Clean up: Delete temporary audio files and directory
for pitch in pitch_range:
    audio_file = os.path.join(temp_dir, f"output_pitch_{pitch}.wav")
    os.remove(audio_file)
os.rmdir(temp_dir)

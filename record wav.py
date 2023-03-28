# Import required libraries
import pyaudio   # For audio input/output
import wave      # For saving audio in WAV format
import keyboard  # For detecting key presses
import time      # For sleeping and debouncing key presses

# Set audio recording parameters
FORMAT = pyaudio.paInt16         # The audio format (16-bit int)
CHANNELS = 1                     # Number of audio channels (1 for mono)
RATE = 44100                     # Audio sampling rate (44.1 kHz)
CHUNK = 1024                     # Audio frames per buffer
WAVE_OUTPUT_FILENAME = "output.wav"  # Output WAV file name

# Initialize the PyAudio library
audio = pyaudio.PyAudio()

# Function to start recording audio
def start_recording():
    # Open an audio stream for input with the specified parameters
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    return stream

# Function to stop recording audio
def stop_recording(stream):
    # Stop the audio stream
    stream.stop_stream()
    # Close the audio stream
    stream.close()

# Function to save recorded audio frames as a WAV file
def save_audio(frames):
    # Open a new WAV file for writing binary data
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    # Set the audio channels, sample width, and frame rate for the WAV file
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    # Write the audio frames to the WAV file
    wf.writeframes(b''.join(frames))
    # Close the WAV file
    wf.close()

# Main function
def main():
    # Print instructions for the user
    print("Press 'k' key to start recording. Press 'k' again to stop and save the recording.")
    
    # Initialize an empty list for storing audio frames
    frames = []
    
    # Initialize a variable to track recording state (True if recording, False otherwise)
    recording = False

    # Main loop
    while True:
        try:
            # Check if the 'k' key is pressed
            if keyboard.is_pressed('k'):
                # Debounce the key press to avoid multiple triggering
                time.sleep(0.2)
                
                # Toggle the recording state
                if not recording:
                    # If not recording, start recording and update the state
                    print("Recording started.")
                    stream = start_recording()
                    recording = True
                else:
                    # If recording, stop recording, save the audio, and exit the loop
                    stop_recording(stream)
                    save_audio(frames)
                    print(f"Recording saved to {WAVE_OUTPUT_FILENAME}")
                    break
            
            # If recording, read audio data from the stream and add it to the frames list
            if recording:
                data = stream.read(CHUNK)
                frames.append(data)
            
            # Sleep for a short period to reduce CPU usage
            time.sleep(0.01)
        
        # Allow the user to exit the script using Ctrl+C
        except KeyboardInterrupt:
            break

    # Terminate the PyAudio library
    audio.terminate()

# Run the main function when the script is executed
if __name__ == '__main__':
    main()

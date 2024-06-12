import subprocess
import speech_recognition as sr
import os

def convert_audio(input_path, output_path):
    """Convert the audio file using ffmpeg and save to a temporary file."""
    try:
        # Run ffmpeg command and suppress its output
        subprocess.run([
            'ffmpeg', '-loglevel', 'quiet', '-i', input_path, '-y', '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', output_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during audio conversion: {e}")
        return False

def recognize_speech(file_path):
    """Recognize speech from the audio file using Google Web Speech API."""
    r = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_text = r.listen(source)
            # Recognize speech using Google Web Speech API
            result = r.recognize_google(audio_text, show_all=True)
            # Extract the transcript
            transcript = ""
            if result and 'alternative' in result:
                transcript = result['alternative'][0]['transcript']
                return transcript
            else:
                return "No transcript found"
    except ValueError as e:
        return f"ValueError: {e}"
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    # Path to the audio files
    input_file_path = 'D:\\integration1\\integration\\media\\audio\\temp.wav'
    temp_output_file_path = 'D:\\integration1\\integration\\media\\audio\\temp_converted.wav'

    # Check if the input file exists
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"The file {input_file_path} does not exist")

    # Convert the audio file
    if convert_audio(input_file_path, temp_output_file_path):
        # Replace the original file with the converted one
        os.replace(temp_output_file_path, input_file_path)
        # Recognize speech from the converted file
        transcript = recognize_speech(input_file_path)
        print(transcript)  # Print only the transcript
    else:
        print("Audio conversion failed.")

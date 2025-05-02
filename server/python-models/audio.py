import ffmpeg
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

# Extract audio from video using ffmpeg
def extract_audio_from_video(video_path, audio_path):
    try:
        ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True)
        print(f"Audio extracted to {audio_path}")
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e}")

# Transcribe audio to text in chunks
def transcribe_audio_in_chunks(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    duration = len(audio)  # Duration of the audio in milliseconds
    recognizer = sr.Recognizer()
    full_text = ''
    
    # Split the audio into 30-second chunks
    for i in range(0, duration, 30000):  # 30-second chunks (30,000 ms)
        chunk = audio[i:i+30000]

        # Convert the chunk to a file-like object in memory
        chunk_io = BytesIO()
        chunk.export(chunk_io, format="wav")
        chunk_io.seek(0)

        # Perform speech recognition on the in-memory chunk
        with sr.AudioFile(chunk_io) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                full_text += text + ' '
            except sr.UnknownValueError:
                full_text += "[Unintelligible] "
            except sr.RequestError as e:
                full_text += f"[Error: {e}] "
    
    return full_text

# Paths
video_path = "sample_video1.mp4"  # Replace with the path to your video file
audio_path = "extracted_audio.wav"  # Temporary audio file

# Extract audio from video
extract_audio_from_video(video_path, audio_path)

# Transcribe the extracted audio
transcript = transcribe_audio_in_chunks(audio_path)

# Print the transcript
print("Transcript:\n", transcript)

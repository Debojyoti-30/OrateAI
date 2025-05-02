import ffmpeg
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import numpy as np
import parselmouth
import librosa
import requests
import matplotlib.pyplot as plt
import re
from collections import Counter
import google.generativeai as genai

genai.configure(api_key="AIzaSyBujSClaWrqfhMTmwTcXcs5a36ttDmU2Y0")

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
    duration = len(audio)
    recognizer = sr.Recognizer()
    full_text = ''

    for i in range(0, duration, 30000):
        chunk = audio[i:i+30000]
        chunk_io = BytesIO()
        chunk.export(chunk_io, format="wav")
        chunk_io.seek(0)

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

# Analyze pitch of the audio
def analyze_pitch(audio_path):
    snd = parselmouth.Sound(audio_path)
    pitch = snd.to_pitch()
    pitch_values_all = pitch.selected_array['frequency']
    time_all = pitch.xs()
    voiced_mask = pitch_values_all != 0
    pitch_values = pitch_values_all[voiced_mask]
    time = time_all[voiced_mask]
    mean_pitch = np.mean(pitch_values)
    return mean_pitch, pitch_values, time

# Analyze speed (words per minute)
def analyze_speed(audio_path):
    y, sr = librosa.load(audio_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    tempo = float(tempo[0])
    duration_in_minutes = librosa.get_duration(y=y, sr=sr) / 60
    words_per_minute = tempo * 1.6
    return words_per_minute, onset_env, sr

# Plot pitch over time
def plot_pitch(time, pitch_values):
    plt.figure(figsize=(10, 4))
    plt.plot(time, pitch_values, color="purple")
    plt.xlabel("Time (s)")
    plt.ylabel("Pitch (Hz)")
    plt.title("Pitch Contour Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plot onset strength (energy onsets)
def plot_onset_strength(onset_env, sr):
    frames = np.arange(len(onset_env))
    times = librosa.frames_to_time(frames, sr=sr)
    plt.figure(figsize=(10, 4))
    plt.plot(times, onset_env, color="green")
    plt.xlabel("Time (s)")
    plt.ylabel("Onset Strength")
    plt.title("Energy Onsets (Speech Activity)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Comment on the speech based on pitch and speed
def comment_on_speech(pitch, speed):
    print("\nSpeech Analysis Report:")
    if 100 <= pitch <= 200:
        print("- Pitch is within a healthy speaking range. Good vocal tone!")
    elif pitch < 100:
        print("- Pitch is quite low. Try to add more energy to your voice.")
    else:
        print("- Pitch is quite high. A calmer tone might sound more relaxed.")
    if 140 <= speed <= 180:
        print("- Speaking speed is excellent! Clear and understandable.")
    elif speed < 140:
        print("- You are speaking a bit slowly. Try to be slightly more lively.")
    else:
        print("- Speaking too fast. Try pausing a little more for clarity.")
    print("\nSuggestions:")
    if not (100 <= pitch <= 200):
        print("• Practice speaking exercises to stabilize your pitch.")
    if not (140 <= speed <= 180):
        print("• Practice controlled breathing and use small pauses while speaking.")
    if (100 <= pitch <= 200) and (140 <= speed <= 180):
        print("• Great job! Just keep practicing for even better modulation!")

# Identify gender based on pitch
def identify_gender(pitch):
    if pitch < 165:
        return "Male"
    elif pitch >= 165:
        return "Female"
    else:
        return "Unknown"

# Calculate score based on pitch and speed
def calculate_score(pitch, speed):
    score = 0
    if 100 <= pitch <= 200:
        score += 5
    elif 80 <= pitch < 100 or 200 < pitch <= 220:
        score += 3
    else:
        score += 1
    if 140 <= speed <= 180:
        score += 5
    elif 120 <= speed < 140 or 180 < speed <= 200:
        score += 3
    else:
        score += 1
    return min(score, 10)

genai.configure(api_key="YOUR_GEMINI_API_KEY")

def generate_gemini_feedback(pitch, speed, gender, filler_counts, transcript):
    model = genai.GenerativeModel('gemini-pro')

    # Prepare prompt
    prompt = f"""
    You are an expert speech evaluator.

    I have the following data from a speaker:
    - Pitch: {pitch:.2f} Hz
    - Speed: {speed:.2f} words per minute
    - Gender: {gender}
    - Filler Words: {filler_counts}
    - Transcript: "{transcript[:1000]}"  # truncated if too long

    Based on this data, give 4 key insights in clear bullet points:
    1. How confident did the speaker sound?
    2. How engaging was the pitch?
    3. How frequently were filler words used and how can it improve?
    4. Any guess on hand gestures and their impact?
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating feedback: {str(e)}"

# --- New Enhancements Below ---

def calculate_voice_clarity(transcript, audio_path):
    total_duration = AudioSegment.from_wav(audio_path).duration_seconds
    intelligible_words = len([word for word in transcript.split() if word not in ["[Unintelligible]", "[Error:"]])
    words_per_second = intelligible_words / total_duration if total_duration else 0
    clarity_score = min(100, words_per_second * 15)
    return round(clarity_score, 2), round(total_duration, 2)

def detect_filler_words(transcript):
    fillers = ['um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 'okay', 'i mean']
    transcript_words = transcript.lower().split()
    filler_counts = {f: transcript_words.count(f) for f in fillers if f in transcript_words}
    total_fillers = sum(filler_counts.values())
    return filler_counts, total_fillers

def analyze_tone_stability(pitch_values):
    std_dev = np.std(pitch_values)
    if std_dev < 30:
        return "Monotonous", round(std_dev, 2)
    elif std_dev < 60:
        return "Moderately expressive", round(std_dev, 2)
    else:
        return "Highly expressive", round(std_dev, 2)

# def suggest_judge_questions(transcript):
#     keywords = re.findall(r'\b\w+\b', transcript.lower())
#     top_keywords = [word for word, freq in Counter(keywords).most_common(5) if len(word) > 4]
#     questions = [f"Can you elaborate more on '{kw}'?" for kw in top_keywords]
#     return questions

# --- Main Process ---

def main(video_path):
    audio_path = "extracted_audio.wav"
    extract_audio_from_video(video_path, audio_path)

    transcript = transcribe_audio_in_chunks(audio_path)
    print("Transcript:\n", transcript)

    pitch, pitch_values, time = analyze_pitch(audio_path)
    speed, onset_env, sr = analyze_speed(audio_path)

    plot_pitch(time, pitch_values)
    plot_onset_strength(onset_env, sr)

    comment_on_speech(pitch, speed)
    gender = identify_gender(pitch)
    score = calculate_score(pitch, speed)
    print(f"\nOverall Score: {score}/10")

    # New integrated insights
    clarity_percent, duration_sec = calculate_voice_clarity(transcript, audio_path)
    print(f"\nVoice Clarity: {clarity_percent}% over {duration_sec} seconds")

    filler_counts, total_fillers = detect_filler_words(transcript)
    print(f"\nFiller Words Detected: {total_fillers}")
    for word, count in filler_counts.items():
        print(f" - {word}: {count} times")

    tone_quality, tone_variance = analyze_tone_stability(pitch_values)
    print(f"\nTone Analysis: {tone_quality} (Variance: {tone_variance})")

    feedback = generate_gemini_feedback(pitch, speed, gender, filler_counts, transcript)
    print("AI Feedback:", feedback)

    # questions = suggest_judge_questions(transcript)
    # print("\nSuggested Questions a Judge Might Ask:")
    # for q in questions:
    #     print(" •", q)

# Run with a sample video
video_path = "sample_video1.mp4"
main(video_path)

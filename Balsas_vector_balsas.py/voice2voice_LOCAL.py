import os
import asyncio
import edge_tts
import pygame
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import subprocess

# --- Optional: add ffmpeg to PATH manually ---
ffmpeg_path = r"C:\ffmpeg\bin"
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ.get("PATH", "")

# --- 1. Record voice ---
def record_audio(filename="audio.wav", duration=6, samplerate=16000):
    print("🎤 Speak now...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    write(filename, samplerate, audio)
    print("✅ Audio recorded.")

# --- 2. Transcribe speech with Whisper ---
def transcribe_audio(filename="audio.wav"):
    print("🔍 Transcribing...")
    model = whisper.load_model("base")
    result = model.transcribe(filename, language="en")
    print("📝 You said:", result["text"])
    return result["text"]

# --- 3. Ask local LLM (gemma3:1b) ---
def ask_local_llm(user_input, model="gemma3:1b"):
    print("🧠 Asking local AI...")
    full_prompt = f"""SYSTEM: Answer concisely in English.

USER: {user_input}
"""
    result = subprocess.run(
        ["ollama", "run", model, full_prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    response = result.stdout.strip()
    print("💬 AI says:", response)
    return response

# --- 4. Convert text to speech (English voice) ---
async def generate_tts(text, filename="response.mp3", voice="en-US-AriaNeural"):
    print("🗣️ Generating speech...")
    tts = edge_tts.Communicate(text, voice=voice)
    await tts.save(filename)

# --- 5. Play the voice file ---
def play_audio(filename="response.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    print("🎬 Done.")

# --- 6. Full cycle ---
def full_cycle():
    record_audio()
    question = transcribe_audio()
    answer = ask_local_llm(question)
    asyncio.run(generate_tts(answer))
    play_audio()

# --- Run the program ---
if __name__ == "__main__":
    full_cycle()

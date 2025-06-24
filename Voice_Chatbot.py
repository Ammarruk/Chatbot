# --------------------------------------------------------
# Imports
# --------------------------------------------------------
import platform
import subprocess
import os
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings

# ... other functions above ...

# ----------------------------
# Stop Audio Playback (Windows only for now)
# ----------------------------
def stop_audio_playback():
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.call(["taskkill", "/IM", "powershell.exe", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_name == "Darwin":
            subprocess.call(["killall", "afplay"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_name == "Linux":
            subprocess.call(["pkill", "aplay"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"❌ Error stopping audio: {e}")


# --------------------------------------------------------
# ElevenLabs API Client Setup
# --------------------------------------------------------
client = ElevenLabs(api_key="sk_dddb029aac074a7c295ef1d585eca0c127bab8bde5307760")

# --------------------------------------------------------
# Convert MP3 to WAV
# --------------------------------------------------------
def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

# --------------------------------------------------------
# Play Audio (WAV only)
# --------------------------------------------------------
def play_audio(audio_path):
    os_name = platform.system()
    print(f"🔊 Playing audio: {audio_path}")
    try:
        if os_name == "Windows":
            subprocess.run([
                "powershell", "-c",
                f'(New-Object Media.SoundPlayer "{audio_path}").PlaySync();'
            ])
        elif os_name == "Darwin":
            subprocess.run(["afplay", audio_path])
        elif os_name == "Linux":
            subprocess.run(["aplay", audio_path])
        else:
            raise OSError("Unsupported OS")
    except Exception as e:
        print(f"❌ Could not play audio: {e}")

# --------------------------------------------------------
# Text to Speech using gTTS
# --------------------------------------------------------
def text_to_speech_with_gtts(input_text, mp3_path="gtts_output.mp3", wav_path="gtts_output.wav"):
    tts = gTTS(text=input_text, lang="en", slow=False)
    tts.save(mp3_path)
    convert_mp3_to_wav(mp3_path, wav_path)
    play_audio(wav_path)

# --------------------------------------------------------
# Text to Speech using ElevenLabs
# --------------------------------------------------------
def text_to_speech_with_elevenlabs(text, output_path="el_output.mp3"):
    audio_stream = client.text_to_speech.convert(
        voice_id="EXAVITQu4vr4xnSDxMaL",  # Rachel
        model_id="eleven_turbo_v2",
        text=text,
        output_format="mp3_22050_32",
        voice_settings={
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    )

    with open(output_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    wav_output = output_path.replace(".mp3", ".wav")
    convert_mp3_to_wav(output_path, wav_output)
    play_audio(wav_output)

# --------------------------------------------------------
# Optional: Test Function (Run if file executed directly)
# --------------------------------------------------------
def run_voice_test():
    el_text = "Hello, this is AI with Ammar."
    text_to_speech_with_elevenlabs(el_text)

# Only run test if this file is executed directly
if __name__ == "__main__":
    run_voice_test()

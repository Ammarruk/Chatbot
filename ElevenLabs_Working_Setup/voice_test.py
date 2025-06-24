from elevenlabs import generate, save, set_api_key
import subprocess
import platform

# Set your API Key here
set_api_key("your_elevenlabs_api_key")  # Replace this!

def play_audio(file_path):
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run(["powershell", "-c", f'(New-Object Media.SoundPlayer \"{file_path}\").PlaySync();'])
        elif os_name == "Darwin":
            subprocess.run(["afplay", file_path])
        elif os_name == "Linux":
            subprocess.run(["aplay", file_path])
        else:
            raise Exception("Unsupported OS")
    except Exception as e:
        print(f"Could not play audio: {e}")

# Generate speech
audio = generate(
    text="This is a working ElevenLabs voice test. Built by Ammar.",
    voice="Rachel",
    model="eleven_turbo_v2"
)

# Save and play
save(audio, "output.mp3")
play_audio("output.mp3")

import logging
from pydub import AudioSegment
from io import BytesIO
import speech_recognition as sr
import os

# ✅ Logging setup only
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path="voicetest.mp3"):
    recognizer = sr.Recognizer()
    mic_index = 1  # ✅ Use correct mic index from earlier

    try:
        with sr.Microphone(device_index=mic_index) as source:
            logging.info("Adjusting for ambient noise (0.5 sec)...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            logging.info("Start speaking. Recording will stop after silence...")

            # ✅ Record until short silence is detected
            audio_data = recognizer.listen(source)
            logging.info("Recording done. Saving to file...")

            # ✅ Convert WAV to MP3
            wave_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wave_data))
            audio_segment.export(file_path, format="mp3", bitrate="192k")

            logging.info(f"✅ Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"❌ An error occurred while recording audio: {e}")
audio_filepath="voicetest.mp3"


record_audio(file_path=audio_filepath)



from groq import Groq
import os

Groq_API_Key = os.environ.get("Groq_API_Key")  # Or directly paste key here
client = Groq(api_key=Groq_API_Key)

stt_model = "whisper-large-v3"
audio_filepath = "voicetest.mp3"

with open(audio_filepath, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language="en"  # You can change to "ur" or "ar" for Urdu/Arabic
    )

print(transcription.text)
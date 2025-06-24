# ✅ Enhanced Gradio App: AmmarGPT with Improved UI/UX Design

import gradio as gr
import speech_recognition as sr
import os
import re
import tempfile
import datetime
try:
    from Chatbot import get_response_from_bot
    from Voice_Chatbot import text_to_speech_with_elevenlabs, stop_audio_playback
except ImportError as e:
    print(f"Error importing Chatbot or Voice_Chatbot modules: {e}")
    raise

# ------------------------------
# Voice Chat Function
# ------------------------------
def handle_voice_input(audio_file):
    if not audio_file:
        return "", None, "🎤 Please record a voice message first."
    
    recognizer = sr.Recognizer()
    try:
        if isinstance(audio_file, dict):  # Handle Gradio's audio file format
            audio_file = audio_file["name"]
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)
            user_text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "", None, "❌ Could not understand audio. Please speak clearly."
    except sr.RequestError as e:
        return "", None, f"❌ Speech recognition error: {e}"
    except Exception as e:
        return "", None, f"❌ Error processing audio: {e}"

    try:
        bot_reply = get_response_from_bot(user_text)
        clean_reply = re.sub(r"[*_`~]", "", bot_reply).strip()
        
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            output_path = tmp_file.name
            try:
                text_to_speech_with_elevenlabs(clean_reply, output_path)
            except Exception as e:
                return user_text, None, f"❌ ElevenLabs TTS error: {e}"
        
        return user_text, output_path, clean_reply
    except Exception as e:
        return user_text, None, f"❌ Bot processing error: {e}"

# ------------------------------
# Text Chat Function
# ------------------------------
def handle_text_input(user_text):
    if not user_text.strip():
        return "", "❌ Please enter a message."
    
    try:
        bot_reply = get_response_from_bot(user_text)
        clean_reply = re.sub(r"[*_`~]", "", bot_reply).strip()
        return "", clean_reply
    except Exception as e:
        return user_text, f"❌ Error: {e}"

# ------------------------------
# Stop Voice Function
# ------------------------------
def stop_voice():
    try:
        stop_audio_playback()
        return None, "🔇 Voice stopped."
    except Exception as e:
        return None, f"❌ Error stopping playback: {e}"

# ------------------------------
# Feedback Handler
# ------------------------------
def handle_feedback(feedback):
    if not feedback:
        return "Please select a feedback option."
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("feedback_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {feedback}\n")
        return f"✅ Feedback submitted: {feedback}"
    except Exception as e:
        return f"❌ Error saving feedback: {e}"

# ------------------------------
# UI/UX Design Enhancements
# ------------------------------
"""
UI/UX DESIGN IMPROVEMENTS:
1. COLOR SCHEME: Gradient (#f5f7fa to #e4e8f0), primary #4361ee, secondary #4cc9f0
2. TYPOGRAPHY: Inter, 2rem headings, 1rem body
3. LAYOUT: 16px spacing, 12px corners
4. INTERACTIVE: Hover effects, loading animations
5. ACCESSIBILITY: 4.5:1 contrast, keyboard navigation
6. MOBILE: Stacked layout, 48px tap targets
7. FEEDBACK: Rating system, visual confirmations
"""

# ------------------------------
# Enhanced CSS Styling
# ------------------------------
enhanced_css = """
:root {
  --primary: #4361ee;
  --primary-dark: #3a0ca3;
  --secondary: #4cc9f0;
  --danger: #f72585;
  --text-primary: #2b2d42;
  --text-secondary: #8d99ae;
  --bg-gradient: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.12);
  --radius-lg: 12px;
  --radius-md: 8px;
}

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg-gradient);
  color: var(--text-primary);
}

.chat-container {
  max-width: 600px;
  margin: auto;
  padding: 16px;
}

.gr-markdown h2 {
  font-size: 2rem !important;
  font-weight: 600 !important;
  color: var(--primary-dark) !important;
  text-align: center !important;
  margin-bottom: 1.5rem !important;
}

.gr-tabs {
  background: white !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: var(--shadow-sm) !important;
  padding: 1rem !important;
}

.gr-tab-item {
  padding: 0.75rem 1.5rem !important;
  font-weight: 600 !important;
  border-radius: var(--radius-md) !important;
  transition: all 0.2s ease !important;
}

.gr-tab-item.selected {
  background: var(--primary) !important;
  color: white !important;
}

.gr-textbox textarea, .gr-textbox input {
  font-size: 1rem !important;
  padding: 0.75rem 1rem !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid #e0e0e0 !important;
  transition: border 0.2s ease !important;
}

.gr-textbox textarea:focus, .gr-textbox input:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.2) !important;
  outline: none !important;
}

.send-btn button, .stop-btn button, .secondary-btn button {
  transition: all 0.2s ease !important;
  min-height: 48px !important;
}

.send-btn button {
  background: var(--primary) !important;
  color: white !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  padding: 0.75rem 1.5rem !important;
  border-radius: var(--radius-md) !important;
  width: 100% !important;
  margin-top: 0.75rem !important;
  box-shadow: var(--shadow-sm) !important;
}

.send-btn button:hover {
  background: var(--primary-dark) !important;
  transform: translateY(-1px) !important;
  box-shadow: var(--shadow-md) !important;
}

.stop-btn button {
  background: var(--danger) !important;
  color: white !important;
  font-size: 0.875rem !important;
  padding: 0.5rem 1rem !important;
  border-radius: var(--radius-md) !important;
  margin-top: 0.75rem !important;
  width: 100% !important;
}

.stop-btn button:hover {
  background: #d0006e !important;
  transform: translateY(-1px) !important;
}

.secondary-btn button {
  background: #f9fafb !important;
  color: var(--text-primary) !important;
  border: 1px solid #e0e0e0 !important;
  font-size: 0.875rem !important;
  padding: 0.5rem 1rem !important;
  border-radius: var(--radius-md) !important;
  margin-top: 0.75rem !important;
  width: 100% !important;
}

.secondary-btn button:hover {
  background: #e5e7eb !important;
  transform: translateY(-1px) !important;
}

.response-box {
  background: white !important;
  border-radius: var(--radius-lg) !important;
  padding: 1rem !important;
  font-size: 1rem !important;
  line-height: 1.5 !important;
  box-shadow: var(--shadow-sm) !important;
  border-left: 4px solid var(--primary) !important;
  margin-top: 1rem !important;
}

audio {
  width: 100% !important;
  margin-top: 1rem !important;
  border-radius: var(--radius-lg) !important;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.loading {
  animation: pulse 1.5s infinite;
  color: var(--text-secondary) !important;
  text-align: center !important;
}

@media (max-width: 600px) {
  .chat-container {
    padding: 8px !important;
  }
  .gr-tab-item {
    padding: 0.5rem 0.75rem !important;
    font-size: 0.875rem !important;
  }
  .gr-markdown h2 {
    font-size: 1.5rem !important;
  }
}

button:focus, input:focus, textarea:focus {
  outline: 2px solid var(--primary) !important;
  outline-offset: 2px !important;
}
"""

# ------------------------------
# UI Components
# ------------------------------
def add_welcome_message():
    return gr.Markdown("""
    Welcome to **AmmarGPT**! Get started:
    
    1. 💬 **Text Chat**: Type and send messages
    2. 🎤 **Voice Chat**: Record and send voice
    3. 🛑 **Stop**: Cancel voice playback
    4. 📋 **Copy**: Copy AI responses
    5. 🔄 **Refresh**: Reload if issues occur
    
    Enjoy text and voice responses!
    """)

def create_feedback_component():
    with gr.Row():
        with gr.Column(scale=2):
            feedback = gr.Radio(
                choices=["👍 Helpful", "👎 Needs Improvement", "🤔 Confusing"],
                label="Was this response helpful?",
                interactive=True
            )
        with gr.Column(scale=1):
            submit_feedback = gr.Button("Submit", elem_classes="secondary-btn")
    return feedback, submit_feedback

# ------------------------------
# Gradio App
# ------------------------------
try:
    with gr.Blocks(css=enhanced_css, theme="default") as app:
        gr.Markdown("## 🤖 AmmarGPT – Your AI Assistant", elem_classes="chat-container")
        
        welcome = add_welcome_message()
        
        with gr.Tabs() as tabs:
            with gr.TabItem("💬 Text Chat", id="text_chat"):
                with gr.Column(elem_classes="chat-container"):
                    user_input = gr.Textbox(
                        placeholder="Type your message here...",
                        show_label=False,
                        lines=3,
                        max_lines=6
                    )
                    with gr.Row():
                        send_btn = gr.Button("📤 Send Message", elem_classes="send-btn")
                        clear_btn = gr.Button("🧹 Clear", elem_classes="secondary-btn")
                    text_output = gr.Textbox(
                        label="AI Response",
                        elem_classes="response-box",
                        interactive=False
                    )
                    
                    # Copy Response Button
                    copy_btn = gr.Button("📋 Copy Response", elem_classes="secondary-btn")
                    copy_output = gr.HTML(visible=False)
                    def trigger_copy(response):
                        if not response:
                            return "<script>alert('No response to copy!');</script>"
                        escaped_response = response.replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
                        return f"""
                        <script>
                            navigator.clipboard.write('{escaped_response}').then(() => {{
                                alert('Response copied to clipboard!');
                            }}).catch(err => {{
                                alert('Failed to copy: ' + err);
                            }});
                        </script>
                        """
                    copy_btn.click(
                        fn=trigger_copy,
                        inputs=text_output,
                        outputs=copy_output
                    )
                    
                    feedback, submit_feedback = create_feedback_component()
                    feedback_output = gr.Textbox(visible=False)
                    
                    send_btn.click(
                        fn=handle_text_input,
                        inputs=user_input,
                        outputs=[user_input, text_output]
                    )
                    user_input.submit(
                        fn=handle_text_input,
                        inputs=user_input,
                        outputs=[user_input, text_output]
                    )
                    clear_btn.click(
                        fn=lambda: ("", ""),
                        outputs=[user_input, text_output]
                    )
                    submit_feedback.click(
                        fn=handle_feedback,
                        inputs=feedback,
                        outputs=feedback_output
                    )

            with gr.TabItem("🎤 Voice Chat", id="voice_chat"):
                with gr.Column(elem_classes="chat-container"):
                    gr.Markdown("Record your voice message:")
                    with gr.Row():
                        voice_input = gr.Audio(
                            sources=["microphone"],
                            type="filepath",
                            label="Press to Record",
                            interactive=True
                        )
                        voice_btn = gr.Button("🎙️ Send Voice", elem_classes="send-btn")
                    
                    heard_text = gr.Textbox(
                        label="You said",
                        interactive=False,
                        elem_classes="response-box"
                    )
                    
                    with gr.Group():
                        voice_reply = gr.Audio(
                            label="AI Voice Response",
                            interactive=False
                        )
                        text_reply = gr.Textbox(
                            label="AI Text Response",
                            elem_classes="response-box",
                            interactive=False
                        )
                    
                    with gr.Row():
                        stop_btn = gr.Button("🛑 Stop Playback", elem_classes="stop-btn")
                        replay_btn = gr.Button("🔊 Replay", elem_classes="secondary-btn")
                    
                    stop_note = gr.Textbox(visible=False)

                    voice_btn.click(
                        fn=handle_voice_input,
                        inputs=voice_input,
                        outputs=[heard_text, voice_reply, text_reply]
                    )
                    stop_btn.click(
                        fn=stop_voice,
                        outputs=[voice_reply, stop_note]
                    )
                    replay_btn.click(
                        fn=lambda x: x,
                        inputs=voice_reply,
                        outputs=voice_reply
                    )

        gr.Markdown("""
        <div style="text-align: center; margin-top: 1.5rem; color: var(--text-secondary); font-size: 0.875rem;">
            Need help? Refresh the page or try rephrasing your question.
        </div>
        """)
except Exception as e:
    print(f"Error initializing Gradio app: {e}")
    raise

# Launch with port iteration
if __name__ == "__main__":
    for port in range(7860, 7871):
        try:
            app.launch(
                server_name="0.0.0.0",
                server_port=port,
                share=False,
                show_error=True,
                inbrowser=True
            )
            print(f"Successfully launched on port {port}")
            break
        except OSError as e:
            print(f"Port {port} is in use, trying next port... ({e})")
    else:
        print("Could not find an available port in range 7860-7870. Please free up a port.")
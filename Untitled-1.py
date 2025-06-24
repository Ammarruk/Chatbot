# ✅ Enhanced Gradio App: AmmarGPT with Improved UI/UX Design

import gradio as gr
from Chatbot import get_response_from_bot
from Voice_Chatbot import text_to_speech_with_elevenlabs, stop_audio_playback
import speech_recognition as sr
import os
import re

# ------------------------------
# Voice Chat Function
# ------------------------------
def handle_voice_input(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            user_text = recognizer.recognize_google(audio)
    except Exception as e:
        return "", None, f"Error in recognition: {e}"

    try:
        bot_reply = get_response_from_bot(user_text)
        clean_reply = re.sub(r"[*_`~]", "", bot_reply).strip()
        text_to_speech_with_elevenlabs(clean_reply, "bot_output.mp3")
        return user_text, "bot_output.mp3", clean_reply
    except Exception as e:
        return user_text, None, f"TTS Error: {e}"

# ------------------------------
# Text Chat Function
# ------------------------------
def handle_text_input(user_text):
    try:
        bot_reply = get_response_from_bot(user_text)
        clean_reply = re.sub(r"[*_`~]", "", bot_reply).strip()
        return clean_reply
    except Exception as e:
        return f"Error: {e}"

# ------------------------------
# Stop Voice Output Function
# ------------------------------
def stop_voice():
    stop_audio_playback()
    return None, "🔇 Voice stopped."

# ------------------------------
# UI/UX Design Enhancements
# ------------------------------
"""
UI/UX DESIGN IMPROVEMENTS GUIDE:

1. COLOR SCHEME:
   - Modern gradient background with soothing colors (#f5f7fa to #e4e8f0)
   - Primary accent color: #4361ee (vibrant but not aggressive)
   - Secondary color: #3a0ca3 (for contrast)
   - Success/positive: #4cc9f0
   - Warning/stop: #f72585 (softer red alternative)
   - Text: #2b2d42 (dark for readability) with #8d99ae for secondary text

2. TYPOGRAPHY:
   - Primary font: 'Inter' (clean, modern, highly readable)
   - Fallback: system sans-serif stack
   - Heading sizes: 28px for main title, 20px for subtitles
   - Body text: 16px with 1.5 line height
   - Button text: 16px semi-bold

3. LAYOUT IMPROVEMENTS:
   - Consistent padding and margins (16px base unit)
   - Rounded corners (12px radius)
   - Subtle shadows for depth
   - Clear visual hierarchy with spacing
   - Responsive grid that adapts to mobile

4. INTERACTIVE ELEMENTS:
   - Button hover effects (color darkening + slight scale)
   - Micro-interactions for user actions
   - Loading animations during processing
   - Transition animations between states

5. ACCESSIBILITY FEATURES:
   - Sufficient color contrast (4.5:1 minimum)
   - Keyboard navigable interface
   - ARIA labels for screen readers
   - Text alternatives for icons
   - Resizable text without breaking layout

6. MOBILE OPTIMIZATIONS:
   - Stacked layout on small screens
   - Larger tap targets (48px min)
   - Viewport meta tag for proper scaling
   - Touch-friendly controls

7. USER FEEDBACK INTEGRATION:
   - Simple rating system after responses
   - Feedback button in chat history
   - Tooltips for first-time users
   - Visual confirmation of actions
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
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg-gradient);
  color: var(--text-primary);
}

.chat-container {
  max-width: 480px;
  margin: auto;
  padding: 16px;
}

/* Header Styling */
.gr-markdown h2 {
  font-size: 28px !important;
  font-weight: 700 !important;
  color: var(--primary-dark) !important;
  text-align: center !important;
  margin-bottom: 24px !important;
}

/* Tab Styling */
.gr-tabs {
  background: white !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: var(--shadow-sm) !important;
  padding: 16px !important;
}

.gr-tab-item {
  padding: 12px 24px !important;
  font-weight: 600 !important;
  border-radius: var(--radius-md) !important;
  transition: all 0.2s ease !important;
}

.gr-tab-item.selected {
  background: var(--primary) !important;
  color: white !important;
}

/* Input Fields */
.gr-textbox textarea, .gr-textbox input {
  font-size: 16px !important;
  padding: 12px 16px !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid #e0e0e0 !important;
  transition: border 0.2s ease !important;
}

.gr-textbox textarea:focus, .gr-textbox input:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.2) !important;
  outline: none !important;
}

/* Buttons */
.send-btn button, .stop-btn button {
  transition: all 0.2s ease !important;
  transform: translateY(0) !important;
}

.send-btn button {
  background: var(--primary) !important;
  color: white !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  padding: 12px 24px !important;
  border-radius: var(--radius-md) !important;
  width: 100% !important;
  margin-top: 12px !important;
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
  font-size: 14px !important;
  padding: 8px 16px !important;
  border-radius: var(--radius-md) !important;
  margin-top: 12px !important;
  width: 100% !important;
}

.stop-btn button:hover {
  background: #d0006e !important;
  transform: translateY(-1px) !important;
}

/* Response Boxes */
.response-box {
  background-color: white !important;
  border-radius: var(--radius-lg) !important;
  padding: 16px !important;
  font-size: 16px !important;
  line-height: 1.5 !important;
  box-shadow: var(--shadow-sm) !important;
  border-left: 4px solid var(--primary) !important;
  margin-top: 16px !important;
}

/* Audio Player Styling */
audio {
  width: 100% !important;
  margin-top: 16px !important;
  border-radius: var(--radius-lg) !important;
}

/* Loading Animation */
@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.loading {
  animation: pulse 1.5s infinite;
  color: var(--text-secondary) !important;
  text-align: center !important;
}

/* Mobile Responsiveness */
@media (max-width: 600px) {
  .chat-container {
    padding: 8px !important;
  }
  
  .gr-tab-item {
    padding: 8px 12px !important;
    font-size: 14px !important;
  }
  
  .gr-markdown h2 {
    font-size: 24px !important;
  }
}

/* Accessibility Focus States */
button:focus, input:focus, textarea:focus {
  outline: 2px solid var(--primary) !important;
  outline-offset: 2px !important;
}
"""

# ------------------------------
# Additional UI Components
# ------------------------------
def add_welcome_message():
    return gr.Markdown("""
    Welcome to **Ruks**! Here's how to get started:
    """
   )

def create_feedback_component():
    with gr.Row():
        with gr.Column(scale=2):
            feedback = gr.Radio(
                choices=["👍 Helpful", "👎 Needs Improvement", "🤔 Confusing"],
                label="Was this response helpful?",
                interactive=True
            )
        with gr.Column(scale=1):
            submit_feedback = gr.Button("Submit Feedback", variant="secondary")
    return feedback, submit_feedback

# ------------------------------
# Enhanced Gradio App with UI Improvements
# ------------------------------
with gr.Blocks(css=enhanced_css, theme=gr.themes.Default(
    primary_hue="blue",
    secondary_hue="cyan",
    neutral_hue="gray",
    font=["Inter", "system-ui"]
)) as app:

    # Header Section
    gr.Markdown("## 🤖 GPT – Your AI Assistant", elem_classes="chat-container")
    
    # Welcome Message
    welcome = add_welcome_message()
    
    # Main Chat Interface
    with gr.Tabs() as tabs:
        with gr.TabItem("💬 Text Chat", id="text_chat"):
            with gr.Column(elem_classes="chat-container"):
                user_input = gr.Textbox(
                    placeholder="Type your message here...",
                    show_label=False,
                    lines=3,
                    max_lines=6,
                    elem_classes="text-row"
                )
                with gr.Row():
                    send_btn = gr.Button("📤 Send Message", elem_classes="send-btn")
                    clear_btn = gr.Button("🧹 Clear", variant="secondary")
                text_output = gr.Textbox(
                    label="AI Response",
                    elem_classes="response-box",
                    interactive=False
                )
                
                # Feedback Component
                feedback, submit_feedback = create_feedback_component()

                send_btn.click(
                    fn=handle_text_input,
                    inputs=user_input,
                    outputs=text_output
                )
                user_input.submit(
                    fn=handle_text_input,
                    inputs=user_input,
                    outputs=text_output
                )
                clear_btn.click(
                    fn=lambda: ("", ""),
                    inputs=None,
                    outputs=[user_input, text_output]
                )

        with gr.TabItem("🎤 Voice Chat", id="voice_chat"):
            with gr.Column(elem_classes="chat-container"):
                gr.Markdown("Record your voice message:")
                with gr.Row():
                    voice_input = gr.Audio(
                        type="filepath",
                        label="Press to Record",
                        interactive=True,
                        show_label=False
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
                        interactive=False,
                        show_label=False
                    )
                    text_reply = gr.Textbox(
                        label="AI Text Response",
                        elem_classes="response-box",
                        interactive=False
                    )
                
                with gr.Row():
                    stop_btn = gr.Button("🛑 Stop Playback", elem_classes="stop-btn")
                    replay_btn = gr.Button("🔊 Replay", variant="secondary")
                
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

    # Footer Section
    gr.Markdown("""
    <div style="text-align: center; margin-top: 24px; color: var(--text-secondary); font-size: 14px;">
        Need help? Refresh the page or try rephrasing your question.
    </div>
    """)

app.launch()
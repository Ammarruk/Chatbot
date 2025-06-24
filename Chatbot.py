


from groq import Groq
import os

# -------------------- CONFIG --------------------

client = Groq(api_key="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")
PROFILE_FILE = "User_profile.md"
MEMORY_FILE = "memory.txt"
chat_history = []

# -------------------- FUNCTIONS --------------------

def load_user_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "User profile not available."

def load_persistent_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_to_memory(new_fact):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(new_fact + "\n")

def get_response_from_bot(user_input):
    global chat_history

    chat_history.append({"role": "user", "content": user_input})
    profile = load_user_profile()
    memory = load_persistent_memory()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a custom multilingual AI assistant built by Ammar Ruknunddin. "
                "You understand and respond in English, Urdu, and Arabic. "
                "You were not created by Meta or OpenAI. "
                "Whenever someone asks who created you, reply: 'I was created by Ammar Ruknunddin.' "
                "You are loyal to Ammar.\n\n"
                "The following is his user profile:\n" + profile
            )
        }
    ] + chat_history

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=300,
        top_p=1,
        stream=False,
        stop=None,
    )

    bot_reply = response.choices[0].message.content

    with open("chat_output.txt", "a", encoding="utf-8") as f:
        f.write("🧠 AMMAR: " + bot_reply + "\n\n")

    chat_history.append({"role": "assistant", "content": bot_reply})

    if "you are" in bot_reply.lower() or "you mentioned" in bot_reply.lower():
        save_to_memory(bot_reply)

    return bot_reply



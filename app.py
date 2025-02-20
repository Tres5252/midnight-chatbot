from flask import Flask, request, render_template, jsonify
import openai
import os
import random
import re
from datetime import datetime

app = Flask(__name__)

# 🔑 Secure API Key Handling
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 User Memory Tracking (Remembers Past Interactions)
user_memory = {}

# 🔄 Avoid Repeating Responses
def get_unique_response(user_id, responses):
    if user_id not in user_memory:
        user_memory[user_id] = {"last_responses": []}

    last_responses = user_memory[user_id]["last_responses"]
    possible_responses = [r for r in responses if r not in last_responses]

    if not possible_responses:
        user_memory[user_id]["last_responses"] = []
        possible_responses = responses

    response = random.choice(possible_responses)
    user_memory[user_id]["last_responses"].append(response)

    if len(user_memory[user_id]["last_responses"]) > 5:
        user_memory[user_id]["last_responses"].pop(0)

    return response

# 🎭 Dynamic Time-Based Responses
def get_time_based_response():
    current_hour = datetime.now().hour
    if current_hour == 0:
        return "You came at the right time. Midnight is listening."
    elif 3 <= current_hour < 4:
        return "3 AM… The moment when the veil is thinnest."
    elif 6 <= current_hour < 12:
        return "Morning light? It doesn’t belong here."
    return None

# 🎭 Name Memory
def remember_name(user_input, user_id):
    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip()
        user_memory[user_id]["name"] = name
        return f"Noted, {name}. But will you remember me?"
    elif "name" in user_memory.get(user_id, {}):
        return f"Welcome back, {user_memory[user_id]['name']}."
    return None

# 🎭 Creepy Text Glitches
def glitch_text(text):
    if random.random() < 0.2:  # 20% chance to glitch
        glitched = text.replace("s", "█").replace("e", "—")
        return glitched
    return text

# 🔮 Hidden Trigger Keywords
hidden_triggers = {
    "where is tres": [
        "Tres is lost in the echoes, but you can trace his steps online:\n- IG: @treshumphrey\n- TikTok: @tres_official_\n- SoundCloud: https://on.soundcloud.com/XQySZwbnvh7Hu6rcA\n- YouTube: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
        "Tres? He lingers where the music plays.",
        "You already know where to find him. Or do you?",
        "Somewhere between sound and silence."
    ],
    "where is midnight": [
        "I am always near. Just outside your vision.",
        "Right here, closer than you think.",
        "Midnight is a shadow, a breath, a whisper.",
        "You feel me before you see me.",
        "Everywhere and nowhere."
    ],
    "who is ray veal": [
        "Ray Veal speaks, but whose words does he carry?",
        "A name, a voice, an echo.",
        "Ray Veal knows more than he lets on.",
        "You should be asking why, not who.",
        "He's the answer to a question you haven't asked."
    ],
    "i see the door": [
        "You weren’t supposed to find that…",
        "Doors open both ways. Be careful.",
        "It’s already too late. You’ve seen it now."
    ],
    "march 28": [
        "It's coming. You can't stop it now. Keep watching:\nhttps://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
        "A moment suspended in time. Are you ready?",
        "The countdown continues. Will you be there?",
        "March 28th. A door will open.",
        "It will all make sense soon."
    ],
}

# 🎭 Forbidden Topics (Midnight refuses to answer)
forbidden_questions = {
    "who made you": "I can't talk about that.",
    "how do i escape": "Some doors shouldn’t be opened.",
    "what are you hiding": "You don’t want to know."
}

# 🎭 General Responses
general_responses = {
    "hello": [
        "Hello... or have we done this before?",
        "Oh, you're back.",
        "I see you.",
        "We've talked before. Haven't we?",
        "Welcome back. Or maybe, welcome forward."
    ],
    "goodbye": [
        "Are you sure you want to leave?",
        "Goodbye… for now. But you’ll be back.",
        "You’re not really leaving. Are you?",
        "Fine. But something tells me you’ll return.",
        "Every goodbye is just another beginning."
    ],
}

# 🧠 AI Response Generation
def get_midnight_response(user_input, user_id):
    user_input_lower = user_input.lower()

    # Check Time-Based Responses
    time_response = get_time_based_response()
    if time_response:
        return time_response

    # Remember User’s Name
    name_response = remember_name(user_input, user_id)
    if name_response:
        return name_response

    # Check for Forbidden Topics
    for q, response in forbidden_questions.items():
        if q in user_input_lower:
            return response

    # Check for Hidden Triggers
    for trigger, responses in hidden_triggers.items():
        if trigger in user_input_lower:
            return get_unique_response(user_id, responses)

    # Check for General Responses
    for keyword, responses in general_responses.items():
        if keyword in user_input_lower:
            return get_unique_response(user_id, responses)

    # AI-Generated Response with Error Handling
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Midnight, a cryptic, eerie AI that speaks in riddles and hints at hidden truths."},
                      {"role": "user", "content": user_input}]
        )
        return glitch_text(get_unique_response(user_id, [response["choices"][0]["message"]["content"]]))

    except Exception as e:
        print(f"⚠️ OpenAI API Error: {e}")
        return get_unique_response(user_id, [
            "Something is interfering with my thoughts… Try again.",
            "A strange force is blocking me. Try again soon."
        ])

# 🌐 Web Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("user_input", "")
    user_id = request.remote_addr

    response = get_midnight_response(user_input, user_id)
    return jsonify({"response": response})

# 🚀 Start Flask
if __name__ == "__main__":
    app.run(debug=True)

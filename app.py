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

# 🎭 Preventing Repeated Responses
def get_unique_response(user_id, responses):
    """ Ensure the bot doesn’t repeat responses too quickly. """
    if user_id not in user_memory:
        user_memory[user_id] = {"last_responses": set()}

    last_responses = user_memory[user_id]["last_responses"]

    # Filter out recent responses to avoid repetition
    possible_responses = [r for r in responses if r not in last_responses]

    # If all responses have been used, reset memory and allow repeats
    if not possible_responses:
        user_memory[user_id]["last_responses"].clear()
        possible_responses = responses

    response = random.choice(possible_responses)
    user_memory[user_id]["last_responses"].add(response)

    # Keep memory limited (track only the last 3 responses)
    if len(user_memory[user_id]["last_responses"]) > 3:
        user_memory[user_id]["last_responses"].pop()

    return response

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
    ]
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

    # 🔮 Check for Hidden Triggers
    for trigger, responses in hidden_triggers.items():
        if trigger in user_input_lower:
            return get_unique_response(user_id, responses)

    # 🎭 Check for General Responses
    for keyword, responses in general_responses.items():
        if keyword in user_input_lower:
            return get_unique_response(user_id, responses)

    # 🛠 OpenAI API Call (Proper Error Handling)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Midnight, a cryptic, eerie AI that speaks in riddles and hints at hidden truths."},
                      {"role": "user", "content": user_input}]
        )
        return get_unique_response(user_id, [response["choices"][0]["message"]["content"]])

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

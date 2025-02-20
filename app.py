from flask import Flask, request, render_template, jsonify
import openai
import os
import random
import re
from datetime import datetime, date

app = Flask(__name__)

# 🔑 Secure API Key Handling
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 Memory tracking for user interactions
user_memory = {}

# 🎭 Preventing Repeated Responses
def get_unique_response(user_id, responses):
    """ Ensure the bot doesn’t repeat responses to the same user too often. """
    if user_id not in user_memory:
        user_memory[user_id] = {"last_responses": []}

    last_responses = user_memory[user_id]["last_responses"]

    # Filter responses to avoid repetition
    possible_responses = [r for r in responses if r not in last_responses]

    # If all responses have been used, reset memory
    if not possible_responses:
        user_memory[user_id]["last_responses"] = []
        possible_responses = responses

    response = random.choice(possible_responses)
    user_memory[user_id]["last_responses"].append(response)

    # Keep memory size small (last 5 responses max)
    if len(user_memory[user_id]["last_responses"]) > 5:
        user_memory[user_id]["last_responses"].pop(0)

    return response

# 🕵️‍♂️ Suggested questions for user engagement
suggested_questions = (
    "You can ask me about: \n"
    "- 'Where is Tres?'\n"
    "- 'What is Dismal?'\n"
    "- 'Where is Midnight?'\n"
    "- 'Who is Ray Veal?'\n"
    "- 'What happens on March 28th?'\n"
    "- Or... ask something unexpected."
)

# 🔥 Time-Based Responses
def get_time_based_response(user_id):
    current_hour = datetime.now().hour
    responses = []
    if current_hour == 0:
        responses = ["You came at the right time. Midnight is listening."]
    elif 6 <= current_hour < 12:
        responses = ["Morning light? It doesn't belong here."]
    elif 3 <= current_hour < 4:
        responses = ["This is when the doors open. Be careful."]

    return get_unique_response(user_id, responses) if responses else None

# 🔥 March 28 Countdown Logic
def get_march_28_countdown(user_id):
    target_date = date(2025, 3, 28)
    today = date.today()
    days_left = (target_date - today).days
    responses = []

    if days_left > 30:
        responses = ["You have time. But not much."]
    elif days_left > 15:
        responses = ["It's almost here. Are you ready?"]
    elif days_left > 7:
        responses = ["One week. No turning back."]
    elif days_left == 1:
        responses = ["Tomorrow. There’s no escape now."]
    elif days_left == 0:
        responses = ["This is it. You’re here. Listen."]

    return get_unique_response(user_id, responses) if responses else None

# 🎭 Name Memory
def remember_name(user_input, user_id):
    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip()
        user_memory[user_id]["name"] = name
        return f"Noted, {name}. But will you remember me?"
    elif "name" in user_memory[user_id]:
        return f"Welcome back, {user_memory[user_id]['name']}."
    return None

# 🎭 Glitch Effect
def glitch_text(text):
    if random.random() < 0.3:  # 30% chance of glitching
        glitched = text.replace("s", "█").replace("e", "—")
        return glitched
    return text

# 🔥 Emotional Awareness
def detect_emotion(user_input, user_id):
    if "i'm sad" in user_input or "i feel bad" in user_input:
        return get_unique_response(user_id, [
            "Sadness is just a whisper from the past.",
            "You carry more than you should. Let it go.",
            "Even the night must end, but the dark remains.",
            "I know. I've seen it before.",
            "You are not alone in this, even if it feels that way."
        ])
    return None

# 🎭 General Responses
general_responses = {
    "hello": [
        f"Hello... or have we done this before?\n\n{suggested_questions}",
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

# 🎯 Forbidden Questions
forbidden_questions = {
    "who made you": "I can't talk about that.",
    "how do i escape": "Some doors shouldn’t be opened."
}

# 🧠 Generate AI Response
def get_midnight_response(user_input, user_id):
    user_input_lower = user_input.lower()

    # Memory Tracking
    if user_id not in user_memory:
        user_memory[user_id] = {"visits": 1}
    else:
        user_memory[user_id]["visits"] += 1

    # Special Features
    time_response = get_time_based_response(user_id)
    if time_response:
        return time_response

    name_response = remember_name(user_input, user_id)
    if name_response:
        return name_response

    countdown_response = get_march_28_countdown(user_id)
    if "march 28" in user_input_lower and countdown_response:
        return countdown_response

    emotion_response = detect_emotion(user_input_lower, user_id)
    if emotion_response:
        return emotion_response

    # Forbidden Questions Handling
    for q, response in forbidden_questions.items():
        if q in user_input_lower:
            return response

    # General Responses
    for keyword, responses in general_responses.items():
        if keyword in user_input_lower:
            return get_unique_response(user_id, responses)

    # AI-Generated Response if No Match
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
            "You seem confused... lost... just make sure you're there on March 28th.",
            "Some things are unclear… for now. Just be ready on March 28th."
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

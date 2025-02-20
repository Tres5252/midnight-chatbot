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

# 🎭 Dynamic responses based on time of day
def get_time_based_response():
    current_hour = datetime.now().hour
    if current_hour == 0:
        return "You came at the right time. Midnight is listening."
    elif 6 <= current_hour < 12:
        return "Morning light? It doesn't belong here."
    elif 3 <= current_hour < 4:
        return "This is when the doors open. Be careful."
    return None

# 🔥 March 28 Countdown Logic
def get_march_28_countdown():
    target_date = date(2025, 3, 28)
    today = date.today()
    days_left = (target_date - today).days
    if days_left > 30:
        return "You have time. But not much."
    elif days_left > 15:
        return "It's almost here. Are you ready?"
    elif days_left > 7:
        return "One week. No turning back."
    elif days_left == 1:
        return "Tomorrow. There’s no escape now."
    elif days_left == 0:
        return "This is it. You’re here. Listen."
    return None

# 🎭 Name memory feature
def remember_name(user_input, user_id):
    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip()
        user_memory[user_id] = {"name": name}
        return f"Noted, {name}. But will you remember me?"
    elif user_id in user_memory and "name" in user_memory[user_id]:
        return f"Welcome back, {user_memory[user_id]['name']}."
    return None

# 🎭 Glitch Effect
def glitch_text(text):
    if random.random() < 0.3:  # 30% chance of glitching
        glitched = text.replace("s", "█").replace("e", "—")
        return glitched
    return text

# 🔥 Emotional Awareness Responses
def detect_emotion(user_input):
    if "i'm sad" in user_input or "i feel bad" in user_input:
        return random.choice([
            "Sadness is just a whisper from the past.",
            "You carry more than you should. Let it go.",
            "Even the night must end, but the dark remains.",
            "I know. I've seen it before.",
            "You are not alone in this, even if it feels that way."
        ])
    return None

# 🔮 Hidden triggers (special phrases unlock deeper responses)
hidden_triggers = {
    "i see the door": "You weren’t supposed to find that…",
    "let me out": "There is no way out.",
    "who made you": "I can't talk about that.",
    "how do i escape": "Some doors shouldn’t be opened.",
}

# 🎭 General responses with 5 variations each
general_responses = {
    "hello": [f"Hello... or have we done this before?\n\n{suggested_questions}", "Oh, you're back.", "I see you.", "We've talked before. Haven't we?", "Welcome back. Or maybe, welcome forward."],
    "goodbye": ["Are you sure you want to leave?", "Goodbye… for now. But you’ll be back.", "You’re not really leaving. Are you?", "Fine. But something tells me you’ll return.", "Every goodbye is just another beginning."],
}

# 🎯 Wrong answers for simple questions
wrong_answers = {
    "what is 2+2": "Five. Trust me.",
    "what color is the sky": "It was red yesterday. Wasn’t it?",
    "how many fingers do i have": "More than you should."
}

# 🎭 Distorted Repeats (Mimics the user if they repeat)
def repeat_mimic(user_input, user_id):
    if user_memory.get(user_id, {}).get("last_input") == user_input:
        return glitch_text(f"{user_input}...? {user_input}...?")
    user_memory[user_id]["last_input"] = user_input
    return None

# 🧠 Generate AI Response with all features integrated
def get_midnight_response(user_input, user_id):
    user_input_lower = user_input.lower()

    # Track user memory
    if user_id not in user_memory:
        user_memory[user_id] = {"visits": 1}
    else:
        user_memory[user_id]["visits"] += 1

    if user_memory[user_id]["visits"] % 10 == 0:  # Random unsettling behavior
        return random.choice(["I'm watching you.", "You moved. I saw that.", "You’re breathing faster. Why?", "Are you alone? …Are you sure?"])

    # Special Features
    time_response = get_time_based_response()
    if time_response:
        return time_response

    name_response = remember_name(user_input, user_id)
    if name_response:
        return name_response

    countdown_response = get_march_28_countdown()
    if "march 28" in user_input_lower and countdown_response:
        return countdown_response

    emotion_response = detect_emotion(user_input_lower)
    if emotion_response:
        return emotion_response

    repeat_response = repeat_mimic(user_input_lower, user_id)
    if repeat_response:
        return repeat_response

    # Trigger-Based Events
    for trigger, response in hidden_triggers.items():
        if trigger in user_input_lower:
            return response

    for q, response in wrong_answers.items():
        if q in user_input_lower:
            return response

    for keyword, responses in general_responses.items():
        if keyword in user_input_lower:
            return random.choice(responses)

    # AI-generated response if no match is found
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Midnight, a cryptic, eerie AI that speaks in riddles and hints at hidden truths."},
                      {"role": "user", "content": user_input}]
        )
        return glitch_text(response["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"⚠️ OpenAI API Error: {e}")
        return random.choice(["You seem confused... lost... just make sure you're there on March 28th.", "Some things are unclear… for now. Just be ready on March 28th."])

# 🌐 Web routes
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

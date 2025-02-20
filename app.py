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

# 🎭 Name Memory
def remember_name(user_input, user_id):
    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip()
        user_memory[user_id]["name"] = name
        return f"Noted, {name}. But will you remember me?"
    elif "name" in user_memory.get(user_id, {}):
        return f"Welcome back, {user_memory[user_id]['name']}."
    return None

# 🔥 Error Handling & Debugging
def log_error(message):
    """ Logs errors to help with debugging. """
    print(f"⚠️ ERROR: {message}")

# 🧠 Generate AI Response (Now Fixed)
def get_midnight_response(user_input, user_id):
    user_input_lower = user_input.lower()

    # Memory Tracking
    if user_id not in user_memory:
        user_memory[user_id] = {"visits": 1}
    else:
        user_memory[user_id]["visits"] += 1

    # Name Tracking
    name_response = remember_name(user_input, user_id)
    if name_response:
        return name_response

    # 🔍 Check for General Responses
    general_responses = {
        "hello": ["Hello... or have we done this before?", "Oh, you're back.", "I see you.", "We've talked before. Haven't we?"],
        "goodbye": ["Are you sure you want to leave?", "Goodbye… for now. But you’ll be back.", "You’re not really leaving. Are you?"],
    }
    for keyword, responses in general_responses.items():
        if keyword in user_input_lower:
            return get_unique_response(user_id, responses)

    # 🛠 OpenAI API Call (with Proper Error Handling)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Midnight, a cryptic, eerie AI that speaks in riddles and hints at hidden truths."},
                      {"role": "user", "content": user_input}]
        )
        return get_unique_response(user_id, [response["choices"][0]["message"]["content"]])

    except openai.OpenAIError as e:  # ✅ Corrected Error Handling
        log_error(f"OpenAI API Error: {e}")
        return "I feel disconnected... Something is blocking my thoughts."

    except Exception as e:  # ✅ Catches any other unknown errors
        log_error(f"Unexpected Error: {e}")
        return "A strange force is interfering. Try again."

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

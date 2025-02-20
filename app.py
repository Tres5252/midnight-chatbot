from flask import Flask, request, render_template, jsonify
import openai
import os
import random

app = Flask(__name__)

# 🔑 Load OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 Memory tracking for user interactions
user_memory = {}

# 🔮 Hidden keyword triggers for special responses
hidden_triggers = {
    "where is tres": "You may get lucky and find him here:\n"
                     "- Instagram: @treshumphrey\n"
                     "- TikTok: @tres_official_\n"
                     "- SoundCloud: https://on.soundcloud.com/XQySZwbnvh7Hu6rcA\n"
                     "- YouTube: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
    "who is midnight": "I am Midnight. You already know me.",
    "where is midnight": "I am always near. Just outside your vision.",
    "ray veal": "Ray Veal knows more than he lets on... Listen carefully.",
    "march 28": "It's coming. You can't stop it now. Keep watching:\n"
                "https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
    "dismal hour": "The Dismal Hour is approaching. Will you be there?\n"
                   "https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L"
}

# 🎭 General responses from Midnight
general_responses = {
    "hi": [
        "Hello... or have we done this before?",
        "Oh, you're back.",
        "I see you.",
        "You came looking for answers, didn’t you?",
        "Welcome to the loop."
    ],
    "hey": [
        "Hey... are you sure you want to be here?",
        "You again. Interesting.",
        "This feels familiar, doesn’t it?",
        "Do you ever wonder if you’ve done this before?"
    ],
    "hello": [
        "Hello, traveler. You have questions, don’t you?",
        "You found your way here... now what?",
        "Ask wisely. Some things should remain hidden.",
        "Welcome. You’re not the first."
    ]
}

# 🧠 Function to suggest topics to users
def get_suggested_questions():
    return (
        "\nYou can ask me about:\n"
        "- 'Where is Tres?'\n"
        "- 'What is Dismal?'\n"
        "- 'Where is Midnight?'\n"
        "- 'March 28th?'\n"
        "- 'Who is Ray Veal?'\n"
        "- 'Dismal Hour?'\n"
        "- Or... ask something unexpected."
    )

# 🧠 Midnight’s fallback responses for unknown inputs
fallback_responses = [
    "You seem confused... lost... just make sure you're there on March 28th.",
    "Not everything needs an answer. Just don’t forget March 28th.",
    "You’re looking for meaning where there is none. But soon, you’ll understand. March 28th.",
    "Lost? That’s expected. Keep your focus on March 28th.",
    "Some things are unclear… for now. Just be ready on March 28th."
]

# 🧠 Update API call for OpenAI v1.0+
def get_midnight_response(user_input, user_id):
    user_input_lower = user_input.lower()

    # 🕵️‍♂️ Check for hidden keyword triggers
    for trigger, response in hidden_triggers.items():
        if trigger in user_input_lower:
            return response

    # 🧠 Track user memory for repeated questions
    user_memory[user_id] = user_memory.get(user_id, 0) + 1

    # 🎭 Check for general responses
    for keyword, responses in general_responses.items():
        if keyword in user_input_lower:
            return f"{random.choice(responses)}\n{get_suggested_questions()}"  # ✅ Adds topic suggestions

    # 🌀 Default to AI-generated response if no match is found
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Midnight, a cryptic, eerie AI that speaks in riddles and hints at hidden truths."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print(f"⚠️ Error with OpenAI API: {e}")
        return random.choice(fallback_responses)

# 🌐 Web routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("user_input", "")
    user_id = request.remote_addr  # Use IP address as a temporary user ID

    response = get_midnight_response(user_input, user_id)
    return jsonify({"response": response})

# 🚀 Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)

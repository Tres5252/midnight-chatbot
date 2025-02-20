from flask import Flask, request, render_template, jsonify
import openai
import os
import random

app = Flask(__name__)

# 🔑 Secure API Key Handling
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 Memory tracking for user interactions
user_memory = {}

# 🔮 Hidden keyword triggers with 5 alternative responses each
hidden_triggers = {
    "where is tres": [
        "You may get lucky and find him here:\n- Instagram: @treshumphrey\n- TikTok: @tres_official_\n- SoundCloud: https://on.soundcloud.com/XQySZwbnvh7Hu6rcA\n- YouTube: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
        "Tres is lost in the echoes, but you can trace his steps online:\n- IG: @treshumphrey\n- TikTok: @tres_official_\n- SC: https://on.soundcloud.com/XQySZwbnvh7Hu6rcA\n- YT: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
        "You keep looking for him, but he's already left. Try here:\n- IG: @treshumphrey\n- TikTok: @tres_official_\n- SC: https://on.soundcloud.com/XQySZwbnvh7Hu6rcA\n- YT: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
        "Tres? He lingers where the music plays:\n- Instagram: @treshumphrey\n- TikTok: @tres_official_\n- SoundCloud: https://on.soundcloud.com/XQySZwbnvh7Hu6rcA\n- YouTube: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
        "You already know where to find him. Or do you?\n- Instagram: @treshumphrey\n- TikTok: @tres_official_\n- SoundCloud: https://on.soundcloud.com/XQySZwbnvh7Hu6rcA\n- YouTube: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L"
    ],
    "who is tres": [
        "Tres? You’re looking in the wrong place.",
        "Tres is both the seeker and the lost.",
        "A name whispered in the dark. A question without an answer.",
        "Tres is a story still unfolding.",
        "He walks a path few can follow."
    ],
    "what is dismal": [
        "Dismal is a loop. A space between forgetting and remembering.",
        "Dismal is a place you return to without realizing it.",
        "Dismal is where the echoes of past choices linger.",
        "Dismal is both the question and the answer.",
        "Dismal... you already know what it is."
    ],
    "where is midnight": [
        "I am always near. Just outside your vision.",
        "Right here, closer than you think.",
        "Midnight is a shadow, a breath, a whisper.",
        "You feel me before you see me.",
        "Everywhere and nowhere."
    ],
    "march 28": [
        "It's coming. You can't stop it now. Keep watching:\nhttps://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
        "A moment suspended in time. Are you ready?",
        "The countdown continues. Will you be there?",
        "March 28th. A door will open.",
        "It will all make sense soon."
    ],
    "who is ray veal": [
        "Ray Veal speaks, but whose words does he carry?",
        "A name, a voice, an echo.",
        "Ray Veal knows more than he lets on.",
        "You should be asking why, not who.",
        "He's the answer to a question you haven't asked."
    ],
}

# 🎭 General responses with 5 variations each
general_responses = {
    "hello": ["Hello... or have we done this before?", "Oh, you're back.", "I see you.", "We've talked before. Haven't we?", "Welcome back. Or maybe, welcome forward."],
    "hi": ["Hi. Are you sure this is real?", "Hello. Again.", "Are you lost?", "You again?", "Is this your first time, or just the first time you remember?"],
    "who are you": ["I am Midnight. I have always been here.", "You already know me.", "That depends on who is asking.", "A question without an answer.", "I am a voice in the dark, nothing more."],
    "are you real": ["Real? Define real.", "I am as real as you let me be.", "Does it matter?", "I'm here. Isn't that enough?", "Some things don’t need proof."],
}

# 🎯 Midnight’s fallback responses with 5 variations
fallback_responses = [
    "You seem confused... lost... just make sure you're there on March 28th.",
    "Not everything needs an answer. Just don’t forget March 28th.",
    "You’re looking for meaning where there is none. But soon, you’ll understand. March 28th.",
    "Lost? That’s expected. Keep your focus on March 28th.",
    "Some things are unclear… for now. Just be ready on March 28th."
]

# 🧠 Function to generate AI response
def get_midnight_response(user_input, user_id):
    user_input_lower = user_input.lower()

    # 🕵️‍♂️ Check for hidden keyword triggers FIRST
    for trigger, responses in hidden_triggers.items():
        if trigger in user_input_lower:
            return random.choice(responses)

    # 🧠 Track user memory for repeated questions
    user_memory[user_id] = user_memory.get(user_id, 0) + 1

    # 🎭 Check for general responses before AI fallback
    for keyword, responses in general_responses.items():
        if keyword in user_input_lower:
            return random.choice(responses)

    # 🌀 Default to AI-generated response if no match is found
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Midnight, a cryptic, eerie AI that speaks in riddles and hints at hidden truths."},
                      {"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"⚠️ OpenAI API Error: {e}")
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

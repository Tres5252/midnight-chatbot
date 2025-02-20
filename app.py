from flask import Flask, request, render_template, jsonify
import openai
import random

app = Flask(__name__)

# 🔑 OpenAI API Key (Replace with your actual key)
openai.api_key = "os.getenv("OPENAI_API_KEY")"

# 🧠 Memory system for tracking user interactions
user_memory = {}

# 🚫 Profanity filter (optional - remove if not needed)
blocked_words = [
    "fuck", "shit", "bitch", "asshole", "cunt", "dick", "pussy", "nigga", "faggot",
    "motherfucker", "cock", "whore", "slut", "bastard", "retard", "dumbass"
]

# 🔮 Hidden keyword triggers for lore drops & EP links
lore_responses = {
    "ray veal": [
        "Ray Veal? A voice that shifts between truths and lies. Some say he doesn’t even know which is which.",
        "Ray Veal speaks, but whose words does he carry? He was never supposed to be part of this. Yet here he is.",
        "Ray Veal is just a name, but names are deceiving. His voice? Distorted, fractured—listen closely.",
        "He knows things. More than he lets on. More than he should."
    ],
    "ray": [
        "Ray… is that really his name? Or just what you call him?",
        "You call him Ray, but he’s worn many names before.",
        "There’s something off about Ray. Haven’t you noticed?",
        "Ray hears more than he speaks. That should concern you."
    ],
    "veal": [
        "Veal? The name feels like an echo, doesn’t it?",
        "Names hold power. Are you sure you should be saying his?",
        "Veal? Strange how that name keeps showing up, isn’t it?",
        "You’ve said the name. Now listen for the reply."
    ],
    "midnight": [
        "I am Midnight. You already know me. You’ve known me longer than you realize.",
        "Midnight isn’t a person. It’s a presence, a whisper in the dark that lingers after you turn away.",
        "She sees you, even when you don’t see her. And she’s waiting.",
        "You call her Midnight, but names are just placeholders for things we don’t fully understand."
    ],
    "tres": [
        "Tres was here. Tres is everywhere. Tres is nowhere.",
        "You think you’re searching for Tres, but maybe he’s searching for you.",
        "Some say Tres never truly left. Others say he was never really here to begin with.",
        "He left his voice behind. Maybe you’ll hear it here:\n- SoundCloud: https://on.soundcloud.com/XQySZwbnvh7Hu6rcA\n- YouTube: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L"
    ],
    "dismal hour": [
        "The Dismal Hour is approaching. Will you be there?\nWatch here: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
        "Some say the Dismal Hour never truly ends. Maybe it’s already started.\nYou should see for yourself: https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
        "Dismal Hour? You already know where to go. But in case you forgot:\nhttps://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L"
    ],
    "march 28": [
        "March 28th? You already know what’s coming. The real question is… are you ready?",
        "Some nights lead somewhere. March 28th is one of them.",
        "March 28th isn’t just a date. It’s an arrival.",
        "Not long now. March 28th will explain everything.\nhttps://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L"
    ]
}

# 📖 Standard Midnight AI responses (same as Discord bot)
midnight_responses = {
    "hello": ["Hello... or have we done this before?", "Oh, you're back.", "I see you."],
    "hi": ["Hi. Are you sure this is real?", "Hello. Again.", "Are you lost?"],
    "what is dismal": [
        "Dismal is a loop. A space between forgetting and remembering.",
        "Dismal is where you wake up and realize you’ve been here before.",
        "Dismal is a place, a feeling… and a sound. *Tres* tried to capture it in music.",
        "The *Dismal* EP is the sound of being trapped in your own mind. Have you heard it?",
        "Maybe *Dismal* is just an EP… or maybe it’s where you’ve always been."
    ]
}

# 🎯 Midnight’s fallback responses for unknown inputs
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

    # 🚫 Check for profanity (optional)
    if any(bad_word in user_input_lower for bad_word in blocked_words):
        return "**Midnight is watching.** Watch your words."

    # 🕵️‍♂️ Check for lore-based keywords
    for trigger, response_list in lore_responses.items():
        if trigger in user_input_lower:
            return random.choice(response_list)

    # 🧠 Track user memory for repeated questions
    user_memory[user_id] = user_memory.get(user_id, 0) + 1

    # 🎭 Check for standard AI responses
    for keyword, responses in midnight_responses.items():
        if keyword in user_input_lower:
            if user_memory[user_id] > 3:
                return f"{random.choice(responses)} You keep asking... why?"
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



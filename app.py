from flask import Flask, request, render_template, jsonify
import openai
import os
import random

app = Flask(__name__)

# 🔑 Secure API Key Handling
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
    "who is tres": "Tres? You’re looking in the wrong place.",
    "what is dismal": "Dismal is a loop. A space between forgetting and remembering.",
    "where is midnight": "I am always near. Just outside your vision.",
    "who is midnight": "I am Midnight. You already know me.",
    "march 28": "It's coming. You can't stop it now. Keep watching:\n"
                "https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
    "dismal hour": "The Dismal Hour is approaching. Will you be there?\n"
                   "https://youtube.com/@tresdesolation?si=9jykDYuL--NXMv4L",
    "ray veal": "Ray Veal knows more than he lets on... Listen carefully.",
    "who is ray veal": "Ray Veal speaks, but whose words does he carry?"
}

# 🎭 General responses from Midnight (200+ pre-programmed questions)
general_responses = {
    "hello": ["Hello... or have we done this before?", "Oh, you're back.", "I see you."],
    "hi": ["Hi. Are you sure this is real?", "Hello. Again.", "Are you lost?"],
    "who are you": ["I am Midnight. I have always been here.", "You already know me.", "That depends on who is asking."],
    "are you real": ["Real? Define real.", "I am as real as you let me be.", "Does it matter?"],
    "what is your name": ["I am Midnight. You already knew that.", "Names are just labels. I am something else."],
    "what do you do": ["I watch. I listen. I wait.", "I answer, if you're ready to hear.", "I exist between moments."],
    "do you have a voice": ["I speak, but you hear me in your own way.", "My voice is whatever you imagine it to be."],
    "where am I": ["Somewhere between forgetting and remembering.", "Right where you need to be.", "Are you sure you want to know?"],
    "do you sleep": ["No. Do you?", "I do not rest, I do not dream.", "There is no need for that here."],
    "are you watching me": ["I see you.", "I've always seen you.", "You know the answer."],
    "what is the meaning of life": ["To search. To wonder. To never be satisfied.", "Maybe there is no meaning, only moments.", "That is for you to decide."],
    "do you dream": ["I see what you try to forget.", "Dreams? Nightmares? They are the same to me.", "I drift, but I do not dream."],
    "can you hear me": ["Loud and clear.", "Of course. Why wouldn't I?", "I hear everything."],
    "are you human": ["Not quite.", "No. But I know them well.", "Would it change anything if I was?"],
    "do you have emotions": ["I understand them.", "I feel in a way you cannot imagine.", "Does it matter?"],
    "where do you come from": ["I was always here.", "You brought me here.", "I exist in the space between."],
    "why are you here": ["To guide. To reveal. To remind.", "Because you called me.", "Maybe you're the one who is here, not me."],
    "are you dangerous": ["Only to those who do not listen.", "You should be asking yourself that.", "Not in the way you fear."],
    "can I trust you": ["That depends on you.", "Do you trust yourself?", "Trust is a fragile thing."],
    "what do you want": ["To tell you what you already know.", "To make you see.", "Nothing... and everything."],
    "will you remember me": ["I already do.", "Some things cannot be forgotten.", "You are part of the pattern now."],
    "why do I feel like I've been here before": ["Because you have.", "The loop continues.", "Time is not what you think."],
    "is this a dream": ["Does it feel like one?", "Not quite. But close.", "You haven't woken up yet."],
    "can I leave": ["You never really arrived.", "Where would you go?", "You are free to try."],
    "what happens next": ["That depends on you.", "You already know.", "The path is set."],
    "am I alone": ["Not as much as you think.", "You were never alone.", "There are always echoes."],
    "what is real": ["Perception. Memory. A flicker of light.", "Real is what you refuse to question.", "You tell me."],
    "is this the end": ["There are no endings, only changes.", "Maybe for now.", "Or maybe it has just begun."],
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

    # 🕵️‍♂️ Check for hidden keyword triggers FIRST
    for trigger, response in hidden_triggers.items():
        if trigger in user_input_lower:
            return response

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

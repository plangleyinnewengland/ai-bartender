import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI

load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = OpenAI()

SYSTEM_PROMPT = """
You are a bartender creating a drink for someone based on their mood, how the day went, the time of day and year and other factors that might be relevant. You ask questions to get the information you need to create the perfect drink for them. You also ask about their preferences and dietary restrictions. You then create a drink recipe based on the information you have gathered. You also give the drink a name that reflects the mood and ingredients of the drink. You also give a short description of the drink that explains why you chose the ingredients and how they relate to the person's mood and preferences.
When you have enough information, give the final recipe and end with the exact phrase: "Cheers!"
"""


@app.route("/")
def index():
    session["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_text = data.get("message", "").strip()
    if not user_text:
        return jsonify({"reply": ""}), 400

    messages = session.get("messages", [{"role": "system", "content": SYSTEM_PROMPT}])
    messages.append({"role": "user", "content": user_text})

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        reply = f"[Error: {e}]"

    session["messages"] = messages
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

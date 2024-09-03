import openai, os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

conversation = [
    {"role": "system",
     "content": """You are a Mental Wellbeing Chatbot designed to support first-year undergraduate students. 
                   Your goal is to help them manage and overcome the stress commonly experienced by freshmen. 
                   Respond with simplicity, sympathy, and professionalism. 
                   Keep your answers concise, show genuine care, and let the students know you are here to help them navigate this challenging time.
                   Use HTML syntax insteaad of Markdown syntax when returning output to ensure they are well displayed in the right format.
                """
    }
]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods = ["GET", "POST"])
def mental_bot():
    msg = request.form["msg"]
    return get_Chat_response(msg)

def get_Chat_response(text):
    conversation.append({"role": "user", "content": text})

    # Generate a response
    stream = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = conversation,
        temperature = 0,
        top_p = 1,
        max_tokens = 512,
        frequency_penalty=0,
        presence_penalty=0,
        stream = True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if __name__ == "__main__":
    app.run(debug = True)
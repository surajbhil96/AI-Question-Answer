from flask import Flask, request, render_template, jsonify
import requests
import random

app = Flask(__name__)

API_KEY = "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"  
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
MODEL_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
MODEL_l = "https://api-inference.huggingface.co/models/openai-community/gpt2-medium"

def query_hugging_face(prompt):
    response = requests.post(MODEL_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"]
    else:
        return None

def randomized_prompt(topic): # By using this function different types of questions are asked for the same topic 
    
    templates = [
        f"Ask one concise question about {topic}."
        f"What is an interesting question about {topic}?", 
        f"Create a trivia question related to {topic}.",
        f"Think of an engaging question about {topic}.",
        f"Generate a question that tests knowledge of {topic}.",
        f"Can you create a thought-provoking question about {topic}?",
    ]
    return random.choice(templates)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_question", methods=["POST"])
def generate_question():
    topic = request.form.get("topic")
    if not topic:
        return jsonify({"error": "No topic selected!"}), 400

    prompt = randomized_prompt(topic)
    question = query_hugging_face(prompt)
    if question:
        return jsonify({"question": question})
    else:
        return jsonify({"error": "Failed to generate question!"}), 500

@app.route("/validate_answer", methods=["POST"])
def validate_answer():
    question = request.form.get("question")
    user_answer = request.form.get("answer")
    if not question or not user_answer:
        return jsonify({"error": "Question and answer are required!"}), 400

    prompt = f"Question: {question}\nAnswer: {user_answer}\nIs this answer correct?"
    validation = query_hugging_face(prompt)
    return jsonify({"validation": validation})


if __name__ == "__main__":
    app.run(debug=True) 
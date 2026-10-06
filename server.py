from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "lan_quiz_secret_key"



questions = [
    {
        "question": "Which protocol is connection-oriented?",
        "options": ["TCP", "UDP", "IP", "ARP"],
        "answer": "1"
    },

    {
        "question": "Which device connects different networks?",
        "options": ["Switch", "Router", "Hub", "Repeater"],
        "answer": "2"
    },

    {
        "question": "What does IP stand for?",
        "options": [
            "Internet Protocol",
            "Internal Process",
            "Internet Program",
            "Information Protocol"
        ],
        "answer": "1"
    },

    {
        "question": "Which protocol is connectionless?",
        "options": ["TCP", "UDP", "HTTP", "FTP"],
        "answer": "2"
    },

    {
        "question": "Which layer of the OSI model uses IP?",
        "options": [
            "Transport Layer",
            "Network Layer",
            "Session Layer",
            "Physical Layer"
        ],
        "answer": "2"
    }
]



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():

    name = request.form.get("name")

    if not name:
        return redirect("/")

    # Store player name
    session["name"] = name

    # Create random question order
    question_order = list(range(len(questions)))
    random.shuffle(question_order)

    session["question_order"] = question_order
    session["current_question"] = 0
    session["score"] = 0

    return redirect("/quiz")

@app.route("/quiz")
def quiz():

    if "name" not in session:
        return redirect("/")

    current = session["current_question"]
    question_order = session["question_order"]

    # Quiz completed
    if current >= len(question_order):
        return redirect("/result")

    question_index = question_order[current]

    q = questions[question_index]

    return render_template(
        "quiz.html",
        question=q,
        question_number=current + 1,
        total_questions=len(question_order)
    )




@app.route("/answer", methods=["POST"])
def answer():

    if "name" not in session:
        return redirect("/")

    selected_answer = request.form.get("answer")

    current = session["current_question"]
    question_order = session["question_order"]

    question_index = question_order[current]

    correct_answer = questions[question_index]["answer"]

    if selected_answer == correct_answer:
        session["score"] += 1

    session["current_question"] += 1

    return redirect("/quiz")




@app.route("/result")
def result():

    if "name" not in session:
        return redirect("/")

    name = session["name"]
    score = session["score"]
    total = len(questions)

    return render_template(
        "result.html",
        name=name,
        score=score,
        total=total
    )



if __name__ == "__main__":

    print("--------------------------------")
    print("       LAN QUIZ SERVER")
    print("--------------------------------")
    print("Server started on port 5000")
    print("Waiting for clients...")
    print("--------------------------------")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )
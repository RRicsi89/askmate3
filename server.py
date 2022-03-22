from flask import Flask, render_template, request, redirect
import connections
import utils
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/list")
def list_questions():
    questions = connections.read_data_from_file(connections.QUESTIONS_PATH)
    timestamps = connections.convert_timestamps(questions)
    headers = connections.LIST_HEADERS
    return render_template("list.html", questions=questions, headers=headers, timestamps=timestamps)


@app.route("/question/<question_id>")
def display_question(question_id=None):
    question = connections.get_data(question_id, connections.QUESTIONS_PATH)
    answers = connections.get_answers_from_file(question_id)
    timestamps = connections.convert_timestamps(answers)
    answer_headers = connections.ANSWER_HEADERS
    return render_template("question.html", question=question, answers=answers, answer_headers=answer_headers, timestamps=timestamps)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template("add_question.html")
    elif request.method == "POST":

        image = request.files["image"]
        image.save(os.path.join(connections.IMAGE_FOLDER_PATH, image.filename))

        new_question = {"id": utils.generate_uuid(), "submission_time": utils.get_time(), "view_number": 0, "vote_number":0, "image": f"images/{image.filename}"}
        for key, value in request.form.items():
            new_question[key] = value
        connections.write_to_file(connections.QUESTIONS_PATH, new_question, connections.QUESTION_HEADERS_CSV)
        return redirect(f"/question/{new_question['id']}")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id=None):
    if request.method == "GET":
        question = connections.get_data(question_id, connections.QUESTIONS_PATH)
        return render_template("new_answer.html", question=question)
    if request.method == "POST":
        message = request.form['message']
        new_answer = {"id": utils.generate_uuid(),"submission_time": utils.get_time(),"vote_number": 0,"question_id": question_id,"message": message,"image":None}
        for key, value in request.form.items():
            new_answer[key] = value
        connections.write_to_file(connections.ANSWERS_PATH, new_answer, connections.ANSWER_HEADERS_CSV)
        return redirect(f"/question/{question_id}")



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

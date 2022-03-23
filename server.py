from flask import Flask, render_template, request, redirect
import connections, data_manager

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/list")
def list_questions():
    questions = connections.read_data_from_file(connections.QUESTIONS_PATH)
    timestamps = data_manager.convert_timestamps(questions)
    headers = connections.LIST_HEADERS
    return render_template("list.html", questions=questions, headers=headers, timestamps=timestamps)


@app.route("/question/<int:question_id>")
def display_question(question_id=None):
    question = connections.get_data(question_id, connections.QUESTIONS_PATH)
    answers = connections.get_answers_from_file(question_id)
    answer_headers = connections.ANSWER_HEADERS
    return render_template("question.html", question=question, answers=answers, answer_headers=answer_headers)

@app.route("/question/<int:question_id>/delete")
def delete_question(question_id):
    return redirect("/list")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

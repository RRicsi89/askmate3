import os
from flask import Flask, render_template, request, redirect, url_for
import connections
import utils

app = Flask(__name__)


@app.route("/")
def hello():
    connections.VISITS += 1
    with open("data/security.txt", "r") as file:
        security_code = file.readline()
    if connections.VISITS == int(security_code):
        connections.save_original_vote_numbers()
        questions = connections.read_data_from_file(connections.QUESTIONS_PATH)
        questions.sort(key=lambda dicti: dicti["submission_time"])
        connections.save_data_to_file(questions, connections.QUESTION_HEADERS_CSV)
    return render_template("index.html")


@app.route("/list")
def list_questions():
    questions = connections.read_data_from_file(connections.QUESTIONS_PATH)
    headers = connections.LIST_HEADERS
    dict_keys = connections.DICT_KEYS
    if "order_direction" in request.args.keys():
        args = request.args
        order_direction = args.get("order_direction")
        order_by = args.get("order_by").lower().replace(" ", "_")
        questions = connections.sort_data(questions, order_direction, order_by)
        connections.save_data_to_file(questions, connections.QUESTION_HEADERS_CSV)
    timestamps = connections.convert_timestamps(questions)
    for i in range(len(questions)):
        questions[i]["submission_time"] = timestamps[i]
    return render_template("list.html", questions=questions, headers=headers, timestamps=timestamps, dict_keys=dict_keys)


@app.route("/question/<question_id>")
def display_question(question_id=None):
    question = connections.get_data(question_id, connections.QUESTIONS_PATH)
    answers = connections.get_answers_from_file(question_id)
    timestamps = connections.convert_timestamps(answers)
    answer_headers = connections.ANSWER_HEADERS
    view_number = int(question['view_number'])
    view_number += 1
    question['view_number'] = view_number
    connections.edit_in_file(connections.QUESTIONS_PATH, question, connections.QUESTION_HEADERS_CSV)
    return render_template("question.html", question=question, answers=answers, answer_headers=answer_headers,
                           timestamps=timestamps)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template("add_question.html")
    elif request.method == "POST":
        new_data = {"id": utils.generate_uuid(),
                    "submission_time": utils.get_time(),
                    "view_number": 0,
                    "vote_number": 0}
        image = request.files["image"]
        items = request.form.items()
        connections.save_new_input(new_data, image, items, answer=False)
        connections.save_original_vote_numbers()
        return redirect(f"/question/{new_data['id']}")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id=None):
    if request.method == "GET":
        question = connections.get_data(question_id, connections.QUESTIONS_PATH)
        return render_template("new_answer.html", question=question)
    elif request.method == "POST":
        message = request.form['message']
        new_data = {"id": utils.generate_uuid(),
                      "submission_time": utils.get_time(),
                      "vote_number": 0,
                      "question_id": question_id,
                      "message": message}
        image = request.files["image"]
        items = request.form.items()
        connections.save_new_input(new_data, image, items, answer=True)
        return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id=None):
    question = connections.get_data(question_id, connections.QUESTIONS_PATH)
    if request.method == 'GET':
        return render_template("edit_question.html", question=question, question_id=question_id)
    if request.method == "POST":
        edited_title = request.form["title"]
        edited_message = request.form["message"]

        question = {"id": question_id,
                    "submission_time": utils.get_time(),
                    "view_number": 0,
                    "vote_number": 0,
                    "title": edited_title,
                    "message": edited_message}

        image = request.files["image"]
        if image:
            image.save(os.path.join(connections.IMAGE_FOLDER_PATH, image.filename))
            question["image"] = f"images/{image.filename}"
        connections.edit_in_file(connections.QUESTIONS_PATH, question, connections.QUESTION_HEADERS_CSV)
        connections.save_original_vote_numbers()
        return redirect("/list")


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    all_questions = connections.read_data_from_file(connections.QUESTIONS_PATH)
    for question in all_questions:
        if question["id"] == question_id:
            line_to_be_edited = question
    connections.delete_in_file(connections.QUESTIONS_PATH, line_to_be_edited, connections.QUESTION_HEADERS_CSV)
    return redirect("/list")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    all_answers = connections.read_data_from_file(connections.ANSWERS_PATH)
    for answer in all_answers:
        if answer["id"] == answer_id:
            line_to_be_edited = answer
    connections.delete_in_file(connections.ANSWERS_PATH, line_to_be_edited, connections.ANSWER_HEADERS_CSV)
    question_id = answer["question_id"]
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/<vote>")
def change_vote_number(question_id=None, vote=None):
    current_question = connections.get_data(question_id, connections.QUESTIONS_PATH)
    number = connections.get_vote_number_from_file(current_question)
    if number == int(current_question["vote_number"]):
        connections.edit_in_file(connections.QUESTIONS_PATH,
                                 connections.update_vote_number(current_question, vote),
                                 connections.QUESTION_HEADERS_CSV)
    return redirect("/list")


@app.route("/answer/<answer_id>/<vote>")
def change_vote_number_answer(answer_id=None, vote=None):
    current_answer = connections.get_data(answer_id, connections.ANSWERS_PATH)
    connections.edit_in_file(connections.ANSWERS_PATH,
                             connections.update_vote_number(current_answer, vote),
                             connections.ANSWER_HEADERS_CSV)
    return redirect(url_for('display_question', question_id=current_answer["question_id"]))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

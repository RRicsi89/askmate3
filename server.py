import os
from flask import Flask, render_template, request, redirect, url_for
import data_handler
import utils

app = Flask(__name__)


@app.route("/")
def hello():
    data_handler.VISITS += 1
    with open("data/security.txt", "r") as file:
        security_code = file.readline()
    if data_handler.VISITS == int(security_code):
        data_handler.save_original_vote_numbers()
        questions = data_handler.read_data_from_file(data_handler.QUESTIONS_PATH)
        questions.sort(key=lambda dicti: dicti["submission_time"])
        data_handler.save_data_to_file(questions, data_handler.QUESTION_HEADERS_CSV)
    return render_template("index.html")


@app.route("/list")
def list_questions():
    questions = data_handler.read_data_from_file(data_handler.QUESTIONS_PATH)
    headers = data_handler.LIST_HEADERS
    dict_keys = data_handler.DICT_KEYS
    if "order_direction" in request.args.keys():
        args = request.args
        order_direction = args.get("order_direction")
        order_by = args.get("order_by").lower().replace(" ", "_")
        questions = data_handler.sort_data(questions, order_direction, order_by)
        data_handler.save_data_to_file(questions, data_handler.QUESTION_HEADERS_CSV)
    timestamps = data_handler.convert_timestamps(questions)
    for i in range(len(questions)):
        questions[i]["submission_time"] = timestamps[i]
    return render_template("list.html", questions=questions, headers=headers, timestamps=timestamps, dict_keys=dict_keys)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_handler.get_data(question_id, data_handler.QUESTIONS_PATH)
    answers = data_handler.get_answers_from_file(question_id)
    timestamps = data_handler.convert_timestamps(answers)
    answer_headers = data_handler.ANSWER_HEADERS
    view_number = int(question['view_number'])
    view_number += 1
    question['view_number'] = view_number
    data_handler.edit_in_file(data_handler.QUESTIONS_PATH, question, data_handler.QUESTION_HEADERS_CSV)
    return render_template("answers.html", question=question, answers=answers, answer_headers=answer_headers,
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
        data_handler.save_new_input(new_data, image, items, answer=False)
        data_handler.save_original_vote_numbers()
        return redirect(f"/question/{new_data['id']}")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id=None):
    if request.method == "GET":
        question = data_handler.get_data(question_id, data_handler.QUESTIONS_PATH)
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
        data_handler.save_new_input(new_data, image, items, answer=True)
        return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id=None):
    question = data_handler.get_data(question_id, data_handler.QUESTIONS_PATH)
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
            image.save(os.path.join(data_handler.IMAGE_FOLDER_PATH, image.filename))
            question["image"] = f"images/{image.filename}"
        data_handler.edit_in_file(data_handler.QUESTIONS_PATH, question, data_handler.QUESTION_HEADERS_CSV)
        data_handler.save_original_vote_numbers()
        return redirect("/list")


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    all_questions = data_handler.read_data_from_file(data_handler.QUESTIONS_PATH)
    question_answers = data_handler.get_answers_from_file(question_id, data_handler.ANSWERS_PATH)
    for question in all_questions:
        if question["id"] == question_id:
            line_to_be_edited = question
            for answer in question_answers:
                if answer["question_id"] == question_id:
                    data_handler.delete_in_file(data_handler.ANSWERS_PATH, answer, data_handler.ANSWER_HEADERS_CSV)
    data_handler.delete_in_file(data_handler.QUESTIONS_PATH, line_to_be_edited, data_handler.QUESTION_HEADERS_CSV)
    return redirect("/list")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    all_answers = data_handler.read_data_from_file(data_handler.ANSWERS_PATH)
    for answer in all_answers:
        if answer["id"] == answer_id:
            line_to_be_edited = answer
    data_handler.delete_in_file(data_handler.ANSWERS_PATH, line_to_be_edited, data_handler.ANSWER_HEADERS_CSV)
    question_id = answer["question_id"]
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/<vote>")
def change_vote_number(question_id=None, vote=None):
    current_question = data_handler.get_data(question_id, data_handler.QUESTIONS_PATH)
    number = data_handler.get_vote_number_from_file(current_question)
    if number == int(current_question["vote_number"]):
        data_handler.edit_in_file(data_handler.QUESTIONS_PATH,
                                 data_handler.update_vote_number(current_question, vote),
                                 data_handler.QUESTION_HEADERS_CSV)
    return redirect("/list")


@app.route("/answer/<answer_id>/<vote>")
def change_vote_number_answer(answer_id=None, vote=None):
    current_answer = data_handler.get_data(answer_id, data_handler.ANSWERS_PATH)
    data_handler.edit_in_file(data_handler.ANSWERS_PATH,
                             data_handler.update_vote_number(current_answer, vote),
                             data_handler.ANSWER_HEADERS_CSV)
    return redirect(url_for('display_question', question_id=current_answer["question_id"]))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_the_question(question_id):
    question = data_handler.get_data(question_id, data_handler.QUESTIONS_PATH)
    if request.method == 'GET':
        return render_template('new_comment.html', question=question)
    elif request.method == 'POST':
        return redirect(f'/question/{ question["id"] }')

@app.route('/search', methods=['GET', 'POST'])
def search():
    question = request.args.get('question-input')
    searched_questions = data_handler.get_questions(question)
    return render_template("search-result.html", searched_questions=searched_questions)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

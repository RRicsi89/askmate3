import os
from flask import Flask, render_template, request, redirect, url_for
import data_handler
import delete_functions
import utils

app = Flask(__name__)


@app.route("/")
def hello():
    # data_handler.VISITS += 1
    # with open("data/security.txt", "r") as file:
    #     security_code = file.readline()
    # if data_handler.VISITS == int(security_code):
    #     data_handler.save_original_vote_numbers()
    #     questions = data_handler.read_data_from_file(data_handler.QUESTIONS_PATH)
    #     questions.sort(key=lambda dicti: dicti["submission_time"])
    #     data_handler.save_data_to_file(questions, data_handler.QUESTION_HEADERS_CSV)
    latest_five_question = data_handler.get_latest_five_question()
    print(latest_five_question)
    return render_template("index.html", question_data=latest_five_question)


@app.route("/list")
def list_questions():
    questions = data_handler.get_all_questions()
    headers = data_handler.LIST_HEADERS
    dict_keys = data_handler.DICT_KEYS
    if "order_direction" in request.args.keys():
        order_direction = request.args.get("order_direction")
        order_by = request.args.get("order_by")
        questions = data_handler.sort_all_questions(order_by, order_direction)
    return render_template("list.html", questions=questions, headers=headers, dict_keys=dict_keys)


@app.route("/question/<question_id>")
def display_question(question_id):
    question_data = data_handler.get_question_by_id(question_id)
    answers = data_handler.get_answers_by_question_id(question_id)
    answer_headers = data_handler.ANSWER_HEADERS
    data_handler.update_question_view_number(question_id)
    q_comments = data_handler.get_comment_by_question_id(question_id)
    question_tags = data_handler.get_question_tags(question_id)
    return render_template("answers.html", question_data=question_data,
                           answers=answers,
                           answer_headers=answer_headers,
                           q_comments=q_comments,
                           question_tags=question_tags)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template("add_question.html")
    elif request.method == "POST":
        if request.files["image"]:
            image = request.files["image"]
            image.save(os.path.join(data_handler.IMAGE_FOLDER_PATH, image.filename))
            question_image = f"images/{image.filename}"
        else:
            question_image = "images/no_picture.png"
        submission_time = utils.get_time()
        new_data = [submission_time, 0, 0, request.form.get("title"), request.form.get("message"), question_image]

        data_handler.save_question_to_db(*new_data)
        question_id = data_handler.get_question_id(request.form.get("title"))[0]["id"]
        return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id=None):
    if request.method == "GET":
        question = data_handler.get_question_by_id(question_id)
        question_id = question[0]["id"]
        return render_template("new_answer.html", question_id=question_id)
    elif request.method == "POST":
        if request.files["image"]:
            image = request.files["image"]
            image.save(os.path.join(data_handler.IMAGE_FOLDER_PATH, image.filename))
            answer_image = f"images/{image.filename}"
        else:
            answer_image = "images/no_picture.png"
        submission_time = utils.get_time()
        new_data = [submission_time, 0, question_id, request.form["message"], answer_image]
        data_handler.save_answer_to_db(*new_data)
        return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id=None):
    question = data_handler.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template("edit_question.html", question=question, question_id=question_id)
    if request.method == "POST":
        edited_title = request.form["title"]
        edited_message = request.form["message"]

        if request.files["image"]:
            image = request.files["image"]
            image.save(os.path.join(data_handler.IMAGE_FOLDER_PATH, image.filename))
            question_image = f"images/{image.filename}"
        else:
            question_image = question[0]["image"]
        submission_time = utils.get_time()
        data_handler.edit_question(question_id, edited_title, edited_message, question_image, submission_time)
        return redirect("/list")


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    question_data = data_handler.get_question_by_id(question_id)
    if question_data[0]["image"] != "images/no_picture.png":
        os.remove(f"{data_handler.STATIC_FOLDER_PATH}/{question_data[0]['image']}")
    delete_functions.delete_question(question_id)
    return redirect("/list")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answer_data = data_handler.get_answer_by_id(answer_id)
    question_id = answer_data[0]["question_id"]
    if answer_data[0]["image"] != "images/no_picture.png":
        os.remove(f"{data_handler.STATIC_FOLDER_PATH}/{answer_data[0]['image']}")
    delete_functions.delete_answer(answer_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/<vote>")
def change_vote_number(question_id=None, vote=None):
    question_data = data_handler.get_question_by_id(question_id)
    question_id = question_data[0]["id"]
    data_handler.update_question_vote(question_id, vote)
    return redirect("/list")


@app.route("/answer/<answer_id>/<vote>")
def change_vote_number_answer(answer_id=None, vote=None):
    answer_data = data_handler.get_answer_by_id(answer_id)
    question_id = answer_data[0]["question_id"]
    data_handler.update_answer_vote(answer_id, vote)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_the_question(question_id):
    if request.method == 'GET':
        return render_template('new_q_comment.html', question_id=question_id)
    elif request.method == 'POST':
        comment = request.form['message']
        time = utils.get_time()
        data_handler.insert_into_q_comment(*[question_id, comment, time])
        return redirect(f'/question/{ question_id }')


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_the_answer(answer_id):
    answer_data=data_handler.get_answer_by_id(answer_id)
    question_id=answer_data[0]['question_id']
    if request.method == 'GET':
        return render_template('new_a_comment.html', answer_id=answer_id, question_id=question_id)
    elif request.method == 'POST':
        comment = request.form['message']
        time = utils.get_time()
        data_handler.insert_into_a_comment(*[answer_id, comment, time])
        return redirect(f'/question/{ question_id }')


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer_info = data_handler.get_answer_by_id(answer_id)
    if request.method == 'GET':
        return render_template('edit_answer.html', answer_id=answer_id, answer_info=answer_info)
    elif request.method == 'POST':
        new_info = request.form["answer_text"]
        submission_time = utils.get_time()
        if request.files["image"]:
            image = request.files["image"]
            image.save(os.path.join(data_handler.IMAGE_FOLDER_PATH, image.filename))
            answer_image = f"images/{image.filename}"
        else:
            answer_image = "images/no_picture.png"
        data_handler.save_edited_answer_to_db(sub_time=submission_time, message=new_info, image=answer_image, answer_id=answer_id)
        return redirect(f'/question/{answer_info[0]["question_id"]}')


@app.route('/comment/<comment_id>/edit', methods=["GET", "POST"])
def edit_comment(comment_id):
    comment_info = data_handler.get_comment_by_id(comment_id)
    if comment_info[0]["question_id"] is None:
        answer_data = data_handler.get_answer_by_id(comment_info[0]["answer_id"])
        redirect_info = answer_data[0]["question_id"]
    else:
        redirect_info = comment_info[0]["question_id"]

    if request.method == "GET":
        return render_template('edit_comment.html', comment_id=comment_id, comment_info=comment_info)
    elif request.method == "POST":
        new_info = request.form["comment_text"]
        submission_time = utils.get_time()
        if comment_info[0]["edited_count"] is None:
            edit_count = 1
        else:
            edit_count = comment_info[0]["edited_count"] + 1
        data_handler.edit_comment(message=new_info, submission_time=submission_time, comment_id=comment_id, edited_count=edit_count)
        return redirect(f'/question/{redirect_info}')


@app.route('/comment/<comment_id>/delete', methods=["GET", "POST"])
def delete_comment(comment_id):
    if request.method == "GET":
        return render_template('confirmation.html', comment_id=comment_id)
    elif request.method == "POST":
        comment_data = data_handler.get_comment_by_id(comment_id)
        question_id = comment_data[0]["question_id"]
        if request.form.get("button") == "yes":
            delete_functions.delete_comment(comment_id)
        return redirect(f'/question/{ question_id }')


@app.route('/question/<question_id>/new-tag', methods=["GET", "POST"])
def add_tag_to_question(question_id):
    if request.method == "GET":
        tags = data_handler.get_tag_names()
        return render_template('add_tag.html', question_id=question_id, tags=tags)
    if request.method == "POST":
        tag_names = [tag["name"] for tag in data_handler.get_tag_names()]
        tag_name = request.form.get("tag")
        if tag_name not in tag_names:
            data_handler.add_new_tag(tag_name)
        question_tags = [tag["id"] for tag in data_handler.get_question_tags(question_id)]
        tag_id = data_handler.get_tag_id_by_name(tag_name)
        if tag_id[0]["id"] not in question_tags:
            data_handler.add_question_tag(question_id, tag_id[0]["id"])
        return redirect(f'/question/{ question_id }')


@app.route('/search', methods=['GET', 'POST'])
def search():
    headers = data_handler.LIST_HEADERS
    question = request.args.get("question_input")
    print(question)
    searched_questions = data_handler.get_questions(question)
    return render_template("search-result.html", headers=headers, searched_questions=searched_questions)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_question_tag(question_id, tag_id):
    delete_functions.delete_tag_from_question(question_id, tag_id)
    return redirect(f'/question/{ question_id }')



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

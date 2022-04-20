import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import data_handler
import delete_functions
import utils
from bonus_questions import SAMPLE_QUESTIONS
from datetime import timedelta

app = Flask(__name__)
app.secret_key = b'\xd0p\x89\xb5/\x1d\xa3hY}\x97b\xd7\x15\xc67'
app.permanent_session_lifetime = timedelta(minutes=20)


@app.route("/")
def hello():
    if 'email' in session:
        latest_five_question = data_handler.get_latest_five_question()
        return render_template("index.html", question_data=latest_five_question, email=session['email'], user_id=session['user_id'])
    else:
        latest_five_question = data_handler.get_latest_five_question()
        return render_template("index.html", question_data=latest_five_question)


@app.route("/list")
def list_questions():
    questions = data_handler.get_all_questions()
    headers = data_handler.LIST_HEADERS
    dict_keys = data_handler.DICT_KEYS
    comments = data_handler.get_question_comments()
    if "order_direction" in request.args.keys():
        if request.args.get("order_direction") == "asc":
            order_direction = "asc"
        else:
            order_direction = "desc"
        order_by = request.args.get("order_by")
        questions = data_handler.sort_all_questions(order_by, order_direction)
    if 'email' in session:
        return render_template("list.html", questions=questions, headers=headers, dict_keys=dict_keys,
                               comments=comments, email=session['email'],
                               user_id=session['user_id'])
    else:
        return render_template("list.html", questions=questions, headers=headers, dict_keys=dict_keys,
                               comments=comments)


@app.route("/question/<question_id>")
def display_question(question_id):
    question_data = data_handler.get_question_by_id(question_id)
    answers = data_handler.get_answers_by_question_id(question_id)
    answer_headers = data_handler.ANSWER_HEADERS
    data_handler.update_question_view_number(question_id)
    q_comments = data_handler.get_comment_by_question_id(question_id)
    question_tags = data_handler.get_question_tags(question_id)
    comment_data = data_handler.get_comments()
    if 'email' in session:
        return render_template("question_detail.html", question_data=question_data,
                               answers=answers,
                               answer_headers=answer_headers,
                               q_comments=q_comments,
                               question_tags=question_tags,
                               comments=comment_data,
                               email=session['email'],
                               user_id=session['user_id'])
    else:
        return render_template("question_detail.html", question_data=question_data,
                               answers=answers,
                               answer_headers=answer_headers,
                               q_comments=q_comments,
                               question_tags=question_tags,
                               comments=comment_data)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        if 'email' in session:
            return render_template("add_question.html")
        else:
            # placeholder for user not logged in warning
            return redirect(url_for('hello'))
    elif request.method == "POST":
        if request.files["image"]:
            image = request.files["image"]
            image.save(os.path.join(data_handler.IMAGE_FOLDER_PATH, image.filename))
            question_image = f"images/{image.filename}"
        else:
            question_image = "images/no_picture.png"
        submission_time = utils.get_time()
        new_data = [submission_time, 0, 0, request.form.get("title"), request.form.get("message"), question_image,
                    session['user_id']]

        data_handler.save_question_to_db(*new_data)
        question_id = data_handler.get_question_id(request.form.get("title"))[0]["id"]
        return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id=None):
    if request.method == "GET":
        question = data_handler.get_question_by_id(question_id)
        question_id = question[0]["id"]
        if 'email' in session:
            return render_template("new_answer.html", question_id=question_id)
        else:
            # placeholder for user not logged in warning
            return redirect(url_for('hello'))
    elif request.method == "POST":
        if request.files["image"]:
            image = request.files["image"]
            image.save(os.path.join(data_handler.IMAGE_FOLDER_PATH, image.filename))
            answer_image = f"images/{image.filename}"
        else:
            answer_image = "images/no_picture.png"
        submission_time = utils.get_time()
        new_data = [submission_time, 0, question_id, request.form["message"], answer_image, session['user_id']]
        data_handler.save_answer_to_db(*new_data)
        return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id=None):
    question = data_handler.get_question_by_id(question_id)
    if request.method == 'GET':
        if 'email' in session:
            return render_template("edit_question.html", question=question, question_id=question_id)
        else:
            # placeholder for user not logged in warning
            return redirect(url_for('hello'))
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
    if 'email' in session:
        question_data = data_handler.get_question_by_id(question_id)
        if question_data[0]["image"] != "images/no_picture.png":
            os.remove(f"{data_handler.STATIC_FOLDER_PATH}/{question_data[0]['image']}")
        delete_functions.delete_question(question_id)
        return redirect("/list")
    else:
        # placeholder for user not logged in warning
        return redirect(url_for('hello'))


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    if 'email' in session:
        answer_data = data_handler.get_answer_by_id(answer_id)
        question_id = answer_data[0]["question_id"]
        if answer_data[0]["image"] != "images/no_picture.png":
            os.remove(f"{data_handler.STATIC_FOLDER_PATH}/{answer_data[0]['image']}")
        delete_functions.delete_answer(answer_id)
        return redirect(f"/question/{question_id}")
    else:
        # placeholder for user not logged in warning
        return redirect(url_for('hello'))



@app.route("/question/<question_id>/<vote>")
def change_vote_number(question_id=None, vote=None):
    question_data = data_handler.get_question_by_id(question_id)
    question_id = question_data[0]["id"]
    user_id = question_data[0]["user_id"]
    data_handler.update_question_vote(question_id, vote)
    if vote == "vote_down":
        data_handler.decrease_reputation(user_id)
    elif vote == "vote_up":
        data_handler.increase_reputation(user_id, "question")
    return redirect("/list")


@app.route("/answer/<answer_id>/<vote>")
def change_vote_number_answer(answer_id=None, vote=None):
    answer_data = data_handler.get_answer_by_id(answer_id)
    question_id = answer_data[0]["question_id"]
    user_id = answer_data[0]["user_id"]
    data_handler.update_answer_vote(answer_id, vote)
    if vote == "vote_down":
        data_handler.decrease_reputation(user_id)
    elif vote == "vote_up":
        data_handler.increase_reputation(user_id, "answer")
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_the_question(question_id):
    if request.method == 'GET':
        if 'email' in session:
            return render_template('new_q_comment.html', question_id=question_id)
        else:
            # placeholder for user not logged in warning
            return redirect(url_for('hello'))
    elif request.method == 'POST':
        comment = request.form['message']
        time = utils.get_time()
        data_handler.insert_into_q_comment(*[question_id, comment, time, session['user_id']])
        return redirect('/list')


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_the_answer(answer_id):
    answer_data = data_handler.get_answer_by_id(answer_id)
    question_id = answer_data[0]['question_id']
    if request.method == 'GET':
        if 'email' in session:
            return render_template('new_a_comment.html', answer_id=answer_id, question_id=question_id)
        else:
            # placeholder for user not logged in warning
            return redirect(url_for('hello'))
    elif request.method == 'POST':
        comment = request.form['message']
        time = utils.get_time()
        data_handler.insert_into_a_comment(*[answer_id, comment, time, session['user_id']])
        return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer_info = data_handler.get_answer_by_id(answer_id)
    if request.method == 'GET':
        if 'email' in session:
            return render_template('edit_answer.html', answer_id=answer_id, answer_info=answer_info)
        else:
            # placeholder for user not logged in warning
            return redirect(url_for('hello'))
    elif request.method == 'POST':
        new_info = request.form["answer_text"]
        submission_time = utils.get_time()
        if request.files["image"]:
            image = request.files["image"]
            image.save(os.path.join(data_handler.IMAGE_FOLDER_PATH, image.filename))
            answer_image = f"images/{image.filename}"
        else:
            answer_image = "images/no_picture.png"
        data_handler.save_edited_answer_to_db(sub_time=submission_time, message=new_info, image=answer_image,
                                              answer_id=answer_id)
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
        if 'email' in session:
            return render_template('edit_comment.html', comment_id=comment_id, comment_info=comment_info)
        else:
            # placeholder for user not logged in warning
            return redirect(url_for('hello'))
    elif request.method == "POST":
        new_info = request.form["comment_text"]
        submission_time = utils.get_time()
        if comment_info[0]["edited_count"] is None:
            edit_count = 1
        else:
            edit_count = comment_info[0]["edited_count"] + 1
        data_handler.edit_comment(message=new_info, submission_time=submission_time, comment_id=comment_id,
                                  edited_count=edit_count)

        if comment_info[0]['question_id'] is not None:
            return redirect(f'/list')
        else:
            return redirect(f'/question/{redirect_info}')


@app.route('/comment/<comment_id>/delete', methods=["GET", "POST"])
def delete_comment(comment_id):
    if request.method == "GET":
        if 'email' in session:
            return render_template('confirmation.html', comment_id=comment_id)
        else:
            # placeholder for user not logged in warning
            return redirect(url_for('hello'))
    elif request.method == "POST":
        if request.form.get("button") == "yes":
            delete_functions.delete_comment(comment_id)
        return redirect('/list')


@app.route('/question/<question_id>/new-tag', methods=["GET", "POST"])
def add_tag_to_question(question_id):
    if request.method == "GET":
        tags = data_handler.get_tag_names()
        if 'email' in session:
            return render_template('add_tag.html', question_id=question_id, tags=tags)
        else:
            # placeholder for user not logged in warning
            return redirect(url_for('hello'))
    if request.method == "POST":
        tag_names = [tag["name"] for tag in data_handler.get_tag_names()]
        tag_name = request.form.get("tag")
        if tag_name not in tag_names:
            data_handler.add_new_tag(tag_name)
        question_tags = [tag["id"] for tag in data_handler.get_question_tags(question_id)]
        tag_id = data_handler.get_tag_id_by_name(tag_name)
        if tag_id[0]["id"] not in question_tags:
            data_handler.add_question_tag(question_id, tag_id[0]["id"])
        return redirect(f'/question/{question_id}')


@app.route('/search', methods=['GET', 'POST'])
def search():
    highlight_start = r"<mark>"
    highlight_end = r"</mark>"
    headers = data_handler.LIST_HEADERS
    search_data = request.args.get("question_input")
    searched_questions = data_handler.get_searched_questions(search_data)
    searched_answers = data_handler.get_searched_answers(search_data)
    length_of_search_data = len(search_data)

    utils.insert_highlight_tags(searched_questions, search_data, "title", length_of_search_data, highlight_start,
                                highlight_end)
    utils.insert_highlight_tags(searched_questions, search_data, "message", length_of_search_data, highlight_start,
                                highlight_end)
    utils.insert_highlight_tags(searched_answers, search_data, "message", length_of_search_data, highlight_start,
                                highlight_end)
    return render_template("search-result.html", headers=headers, searched_questions=searched_questions,
                           searched_answers=searched_answers)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_question_tag(question_id, tag_id):
    if 'email' in session:
        delete_functions.delete_tag_from_question(question_id, tag_id)
    else:
        # placeholder for user not logged in warning
        return redirect(url_for('hello'))
    return redirect(f'/question/{question_id}')


@app.route('/users')
def list_users():
    headers = data_handler.USER_LIST_HEADERS
    if "email" in session:
        users = data_handler.get_users_data()
        return render_template('users.html', users=users, headers=headers)
    return redirect('/')


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route('/registration', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('registration_page.html')
    elif request.method == 'POST':
        email = request.form["email"]
        if data_handler.check_user_in_database(email):
            return redirect(url_for('register_user'))
        else:
            password = utils.hash_password(request.form["password"])
            data_handler.create_user_information(email, password)
            return redirect(url_for('hello'))


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form["username"]
        password = request.form["password"]
        if data_handler.check_user_in_database(email):
            if utils.verify_password(password, data_handler.get_hashed_password_by_email(email)[0]["password"]):
                session['email'] = email
                session['user_id'] = data_handler.get_user_id_by_email(email)[0]["id"]
                session.permanent = True
                print(session['user_id'])
                return redirect(url_for('hello'))
            else:
                return render_template('login.html')
        else:
            return render_template('login.html')


@app.route("/user/<user_id>")
def user_profile(user_id):
    all_user_data = data_handler.get_users_data()
    additional_user_details = [user for user in all_user_data if str(user['id']) == user_id]
    user_details = data_handler.get_all_user_info_by_user_id(user_id)
    return render_template("user_profile.html", user_details=user_details, additional_user_details=additional_user_details)


@app.route('/accept-answer/<question_id>/<answer_id>')
def accept_answer(question_id, answer_id):
    answer_data = data_handler.get_answer_by_id(answer_id)
    question_data = data_handler.get_question_by_id(question_id)
    answer_user_id = answer_data[0]["user_id"]
    question_user_id = question_data[0]["user_id"]
    if question_user_id == session["user_id"]:
        data_handler.update_reputation(answer_user_id)
        data_handler.update_acceptance(answer_id, True)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/decline-answer/<question_id>/<answer_id>')
def decline_answer(question_id, answer_id):
    question_data = data_handler.get_question_by_id(question_id)
    question_user_id = question_data[0]["user_id"]
    if question_user_id == session["user_id"]:
        data_handler.update_acceptance(answer_id, False)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/logout')
def logout_user():
    session.pop('email', None)
    session.pop('user_id', None)
    return redirect(url_for('hello'))


@app.route('/tags')
def get_tags():
    tags = data_handler.count_tags()
    return render_template('tag.html', tags=tags)
    pass


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

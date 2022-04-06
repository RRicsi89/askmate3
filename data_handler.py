import csv
import os
import connections


QUESTIONS_PATH = os.getenv('QUESTIONS_PATH') if "QUESTIONS_PATH" in os.environ else "data/questions.csv"
ANSWERS_PATH = os.getenv('ANSWERS_PATH') if "ANSWERS_PATH" in os.environ else "data/answers.csv"
IMAGE_FOLDER_PATH = os.getenv('IMAGE_FOLDER_PATH') if "IMAGE_FOLDER_PATH" in os.environ else "static/images"
VOTE_NUMBERS_PATH = os.getenv('VOTE_NUMBERS_PATH') if "VOTE_NUMBERS_PATH" in os.environ else "data/votes.csv"
SECURITY_CODE_PATH = os.getenv('SECURITY_CODE_PATH') if "VOTE_NUMBERS_PATH" in os.environ else "data/security.txt"
STATIC_FOLDER_PATH = os.getenv('STATIC_FOLDER_PATH') if 'STATIC_FOLDER_PATH' in os.environ else "static"

VISITS = 0

LIST_HEADERS = ["Submission Time", "Number of views", "Number of votes", "Title", "Message"]
ANSWER_HEADERS = ["Submission Time", "Vote Number", "Message", "Image"]
QUESTION_HEADERS_CSV = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS_CSV = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
DICT_KEYS = ["submission_time", "view_number", "vote_number", "title", "message"]


# def read_data_from_file(file=None):
#     with open(file, "r") as csvfile:
#         reader = csv.DictReader(csvfile)
#         return [line for line in reader]

@connections.connection_handler
def get_questions(cursor, searched_question):
    query = f"""
        SELECT DISTINCT
            question.id,
            question.submission_time,
            question.view_number,
            question.vote_number,
            question.title,
            question.message,
            question.image
        FROM question FULL OUTER JOIN answer
        ON question.id = answer.question_id
        WHERE
            LOWER(question.title) LIKE '%{searched_question.lower()}%' OR
            LOWER(question.message) LIKE '%{searched_question.lower()}%' OR
            LOWER(answer.message) LIKE '%{searched_question.lower()}%';
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def get_all_questions(cursor):
    query = """
        SELECT * FROM question
        ORDER BY submission_time;
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def sort_all_questions(cursor, key, direction):
    query = f"""
        SELECT * FROM question
        ORDER BY {key} {direction};
    """
    cursor.execute(query)
    return cursor.fetchall()


# def get_data(data_id, file_to_read_from):
#     datas = read_data_from_file(file_to_read_from)
#     for data in datas:
#         if data["id"] == data_id:
#             return data


@connections.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT * FROM question
        WHERE id = %(question_id)s;
    """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@connections.connection_handler
def get_answer_by_id(cursor, answer_id):
    query = f"""
        SELECT * 
        FROM answer
        WHERE id = {answer_id}
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def get_answers_by_question_id(cursor, question_id):
    query = """
        SELECT answer.id, answer.submission_time, answer.vote_number, answer.message, answer.image FROM answer
        JOIN question
            ON answer.question_id = question.id
        WHERE answer.question_id = %(question_id)s
        ORDER BY answer.id;
    """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@connections.connection_handler
def save_question_to_db(cursor, *args):
    query = f"""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
        VALUES {args}
    """
    cursor.execute(query)


@connections.connection_handler
def get_question_id(cursor, title):
    query = f"""
        SELECT id FROM question
        WHERE title = %(title)s
    """
    cursor.execute(query, {"title": title})
    return cursor.fetchall()


@connections.connection_handler
def save_answer_to_db(cursor, *args):
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image) 
        VALUES {args}
    """
    cursor.execute(query)


@connections.connection_handler
def save_edited_answer_to_db(cursor, sub_time, message, image, question_id):
    query = f"""
    UPDATE answer
    SET submission_time = '{sub_time}',
    message = '{message}',
    image = '{image}'
    WHERE id = '{question_id}'
    """
    cursor.execute(query)


@connections.connection_handler
def insert_into_q_comment(cursor, *args):
    query = f"""
        INSERT INTO comment (question_id, message, submission_time)
        VALUES {args}
    """
    cursor.execute(query)


@connections.connection_handler
def insert_into_a_comment(cursor, *args):
    query = f"""
        INSERT INTO comment (answer_id, message, submission_time)
        VALUES {args}
    """
    cursor.execute(query)


@connections.connection_handler
def get_comment_by_question_id(cursor, question_id):
    query = f"""
        SELECT comment.id, comment.submission_time, comment.message FROM comment
        JOIN question
            ON comment.question_id = question.id
        WHERE comment.question_id = %(question_id)s;
    """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@connections.connection_handler
def edit_question(cursor, question_id, title, message, image, submission_time):
    query = """
        UPDATE question
        SET title = %(title)s,
            message = %(message)s,
            image = %(image)s,
            submission_time = %(submission_time)s
        WHERE id = %(question_id)s
    """
    cursor.execute(query, {"title": title, "message": message, "question_id": question_id, "image": image, "submission_time": submission_time})


@connections.connection_handler
def update_question_vote(cursor, question_id, vote):
    if vote == "vote_up":
        query = """
            UPDATE question
            SET vote_number = vote_number + 1
            WHERE id = %(question_id)s
    """
    elif vote == "vote_down":
        query = """
            UPDATE question
            SET vote_number = vote_number - 1
            WHERE id = %(question_id)s
        """
    cursor.execute(query, {"question_id": question_id})


@connections.connection_handler
def update_answer_vote(cursor, answer_id, vote):
    if vote == "vote_up":
        query = """
            UPDATE answer
            SET vote_number = vote_number + 1
            WHERE id = %(answer_id)s
    """
    elif vote == "vote_down":
        query = """
            UPDATE answer
            SET vote_number = vote_number - 1
            WHERE id = %(answer_id)s
        """
    cursor.execute(query, {"answer_id": answer_id})


@connections.connection_handler
def update_question_view_number(cursor, question_id):
    query = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = %(question_id)s
        """
    cursor.execute(query, {"question_id": question_id})


@connections.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = """
        SELECT * FROM comment
        WHERE id = %(comment_id)s;
    """
    cursor.execute(query, {"comment_id": comment_id})
    return cursor.fetchall()


@connections.connection_handler
def get_tag_names(cursor):
    query = """
        SELECT name FROM tag
        ORDER BY name
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def add_new_tag(cursor, tag_name):
    query = """
        INSERT INTO tag (name)
        VALUES (%(tag_name)s)
    """
    cursor.execute(query, {"tag_name": tag_name})


@connections.connection_handler
def add_question_tag(cursor, question_id, tag_id):
    query = f"""
        INSERT INTO question_tag (question_id, tag_id)
        VALUES ({question_id}, {tag_id})
    """
    cursor.execute(query)


@connections.connection_handler
def get_tag_id_by_name(cursor, tag_name):
    query = """
        SELECT id FROM tag
        WHERE name = %(tag_name)s
    """
    cursor.execute(query, {"tag_name": tag_name})
    return cursor.fetchall()


@connections.connection_handler
def get_latest_five_question(cursor):
    query = """
    SELECT submission_time, view_number, vote_number, title, id
    FROM question
    ORDER BY submission_time desc
    LIMIT 5
    """
    cursor.execute(query)
    return cursor.fetchall()


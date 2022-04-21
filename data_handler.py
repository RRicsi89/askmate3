import os
import connections
from psycopg2 import sql


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
USER_LIST_HEADERS = ["Username", "Registration", "Reputation", "Questions", "Answers", "Comments"]
TAG_HEADERS = ['Tags', 'Quantity']


# def read_data_from_file(file=None):
#     with open(file, "r") as csvfile:
#         reader = csv.DictReader(csvfile)
#         return [line for line in reader]

@connections.connection_handler
def get_searched_questions(cursor, searched_question):
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
def get_searched_answers(cursor, searched_question):
    query = f"""
        SELECT DISTINCT
        answer.id,
        answer.submission_time,
        answer.vote_number,
        answer.message,
        answer.question_id
        FROM answer
        WHERE
        LOWER(answer.message) LIKE '%{searched_question.lower()}%'
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
    query = sql.SQL("""
        SELECT * FROM question
        ORDER BY {key} {direction};
    """).format(key=sql.Identifier(key), direction=sql.SQL(direction))
    cursor.execute(query)
    return cursor.fetchall()


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
        SELECT answer.id, 
                answer.submission_time, 
                answer.vote_number, 
                answer.message, 
                answer.image, 
                answer.user_id,
                answer.accepted
                FROM answer
        JOIN question
            ON answer.question_id = question.id
        WHERE answer.question_id = %(question_id)s
        ORDER BY answer.id;
    """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@connections.connection_handler
def save_question_to_db(cursor, *args):
    query = sql.SQL("""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id) 
        VALUES {args}
    """).format(args=sql.Literal(args))
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
    query = sql.SQL("""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id) 
        VALUES {args}
    """).format(args=sql.Literal(args))
    cursor.execute(query)


@connections.connection_handler
def save_edited_answer_to_db(cursor, sub_time, message, image, answer_id):
    query = sql.SQL("""
    UPDATE answer
    SET submission_time = {sub_time},
    message = {message},
    image = {image}
    WHERE id = {answer_id}
    """).format(
            sub_time=sql.Literal(sub_time),
            message=sql.Literal(message),
            image=sql.Literal(image),
            answer_id=sql.Literal(answer_id)
    )
    cursor.execute(query)


@connections.connection_handler
def insert_into_q_comment(cursor, *args):
    query = sql.SQL("""
        INSERT INTO comment (question_id, message, submission_time, user_id)
        VALUES {args}
    """).format(args=sql.Literal(args))
    cursor.execute(query)


@connections.connection_handler
def insert_into_a_comment(cursor, *args):
    query = sql.SQL("""
        INSERT INTO comment (answer_id, message, submission_time, user_id)
        VALUES {args}
    """).format(args=sql.Literal(args))
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
def get_comments(cursor):
    query = """
        SELECT * FROM comment;
    """
    cursor.execute(query)
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
    cursor.execute(query, {"title": title, "message": message, "question_id": question_id, "image": image,
                           "submission_time": submission_time})


@connections.connection_handler
def edit_comment(cursor, comment_id, message, submission_time, edited_count):
    query = """
    UPDATE comment
    SET message = %(message)s,
        edited_count = %(edited_count)s,
        submission_time = %(submission_time)s
    WHERE id = %(comment_id)s
    
    """
    cursor.execute(query, {"comment_id": comment_id, "message": message, "submission_time": submission_time,
                           "edited_count": edited_count})


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
        ORDER BY id
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
    query = """
        INSERT INTO question_tag (question_id, tag_id)
        VALUES (%(question_id)s, %(tag_id)s)
    """
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})


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


@connections.connection_handler
def get_question_tags(cursor, question_id):
    query = """
        SELECT DISTINCT name, id FROM tag
        JOIN question_tag ON question_tag.tag_id = tag.id
        WHERE question_tag.question_id = %(question_id)s
    """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@connections.connection_handler
def get_question_comments(cursor):
    query = """
        SELECT DISTINCT * FROM comment
        WHERE question_id IS NOT NULL
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def create_user_information(cursor, username, password):
    query = f"""
        INSERT INTO users
        (username, password)
        VALUES ('{username}', '{password}')

    """
    cursor.execute(query)


@connections.connection_handler
def check_user_in_database(cursor, email):
    query = f"""
        SELECT username
        FROM users
        WHERE username = '{email}'
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def get_hashed_password_by_email(cursor, username):
    query = f"""
        SELECT password
        FROM users
        WHERE username = '{username}'
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def get_users_data(cursor):
    query = sql.SQL("""
        SELECT
                users.id,
                users.username,
                TO_CHAR(users.registration_date, 'YYYY-MM-DD hh:mm:ss'),
                users.reputation,
                questions.question_count,
                answers.answer_count,
                comments.comment_count
                FROM users
                JOIN (SELECT users.id AS id, COUNT(question.id) AS question_count FROM users 
                    LEFT JOIN question ON users.id = question.user_id 
                    GROUP BY users.id) AS questions
                    ON questions.id = users.id
                JOIN (SELECT users.id AS id, COUNT(answer.id) AS answer_count FROM users 
                    LEFT JOIN answer ON users.id = answer.user_id 
                    GROUP BY users.id) AS answers
                    ON answers.id = users.id
                JOIN (SELECT users.id AS id, COUNT(comment.id) AS comment_count FROM users 
                    LEFT JOIN comment ON users.id = comment.user_id 
                    GROUP BY users.id) AS comments
                    ON comments.id = users.id
    """)
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def get_all_user_info_by_user_id(cursor, userid):
    query = f"""
        SELECT *
        FROM users
        WHERE id = {userid}
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def update_reputation(cursor, user_id):
    query = sql.SQL("""
        UPDATE users
        SET reputation = reputation + 15
        WHERE id = {user_id}
        """).format(user_id=sql.Literal(user_id))
    cursor.execute(query)


@connections.connection_handler
def update_acceptance(cursor, answer_id, state):
    if state:
        query = sql.SQL("""
            UPDATE answer SET accepted = TRUE
            WHERE id = {answer_id}
        """).format(answer_id=sql.Literal(answer_id))
    else:
        query = sql.SQL("""
            UPDATE answer SET accepted = FALSE
            WHERE id = {answer_id}
        """).format(answer_id=sql.Literal(answer_id))
    cursor.execute(query)


@connections.connection_handler
def get_user_id_by_email(cursor, email):
    query = f"""
    SELECT id FROM users WHERE username = '{email}'
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def decrease_reputation(cursor, user_id):
    query = sql.SQL("""
        UPDATE users SET reputation = reputation - 2
        WHERE id = {user_id}
    """).format(user_id=sql.Literal(user_id))
    cursor.execute(query)


@connections.connection_handler
def count_tags(cursor):
    query = f"""
    SELECT
    tag.name AS tags,
    count(question_tag.tag_id) AS quantity
    FROM tag
    FULL JOIN question_tag
    ON tag.id = question_tag.tag_id
    GROUP BY tag.name
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def increase_reputation(cursor, user_id, data):
    if data == "question":
        query = sql.SQL("""
            UPDATE users SET reputation = reputation + 5
            WHERE id = {user_id}
        """).format(user_id=sql.Literal(user_id))
    elif data == "answer":
        query = sql.SQL("""
            UPDATE users SET reputation = reputation + 10
            WHERE id = {user_id}
        """).format(user_id=sql.Literal(user_id))
    cursor.execute(query)


@connections.connection_handler
def list_questions_by_user_id(cursor, user_id):
    query = f"""
        SELECT submission_time, view_number, vote_number, title, message
        FROM question
        WHERE question.user_id = '{user_id}'
    
    """
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def get_user_questions(cursor, user_id):
    query = sql.SQL("""
        SELECT * FROM question
        WHERE user_id = {user_id}
    """).format(user_id=sql.Literal(user_id))
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def get_user_answers(cursor, user_id):
    query = sql.SQL("""
        SELECT * FROM answer
        WHERE user_id = {user_id}
    """).format(user_id=sql.Literal(user_id))
    cursor.execute(query)
    return cursor.fetchall()


@connections.connection_handler
def get_user_comments(cursor, user_id):
    query = sql.SQL("""
        SELECT * FROM comment
        WHERE user_id = {user_id}
    """).format(user_id=sql.Literal(user_id))
    cursor.execute(query)
    return cursor.fetchall()

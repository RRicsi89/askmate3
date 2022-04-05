import connections


@connections.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %(question_id)s
    """
    cursor.execute(query, {"question_id": question_id})


@connections.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE FROM answer
        WHERE id = %(answer_id)s
    """
    cursor.execute(query, {"question_id": answer_id})


@connections.connection_handler
def delete_comment(cursor, comment_id):
    query = """
        DELETE FROM question
        WHERE id = %(comment_id)s
    """
    cursor.execute(query, {"question_id": comment_id})


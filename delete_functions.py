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
    cursor.execute(query, {"answer_id": answer_id})


@connections.connection_handler
def delete_comment(cursor, comment_id):
    query = """
        DELETE FROM comment
        WHERE id = %(comment_id)s
    """
    cursor.execute(query, {"comment_id": comment_id})


@connections.connection_handler
def delete_tag_from_question(cursor, question_id, tag_id):
    query = """
        DELETE FROM question_tag
        WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
    """
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})


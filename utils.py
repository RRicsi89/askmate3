import datetime
import uuid
import re


def generate_uuid():
    uu_id = uuid.uuid4()
    return str(uu_id)


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def insert_highlight_tags(searched_questions, search_input, what_to_index, length_of_search_data, highlight_start,
                          highlight_end):
    for result_row in searched_questions:
        result = [m.start() for m in re.finditer(search_input.lower(), result_row[what_to_index].lower())]
        for number in result[::-1]:
            result_row[what_to_index] = result_row[what_to_index][:(number + length_of_search_data)] + highlight_end + \
                                        result_row[what_to_index][(number + length_of_search_data):]
            result_row[what_to_index] = result_row[what_to_index][:number] + highlight_start + \
                                        result_row[what_to_index][number:]

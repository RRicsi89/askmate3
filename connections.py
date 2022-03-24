import csv
import os
from datetime import datetime

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


def read_data_from_file(file=None):
    with open(file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return [line for line in reader]


def get_data(data_id, file_to_read_from):
    datas = read_data_from_file(file_to_read_from)
    for data in datas:
        if data["id"] == data_id:
            return data


def get_answers_from_file(question_id, file_to_read_from=ANSWERS_PATH):
    answer_data = read_data_from_file(file_to_read_from)
    answers = []
    for data in answer_data:
        if data["question_id"] == question_id:
            answers.append(data)
    return answers


def convert_timestamps(dictionaries):
    timestamps = []
    for dictionary in dictionaries:
        for key, value in dictionary.items():
            if key == "submission_time":
                timestamps.append(datetime.fromtimestamp(int(value)))
    return timestamps


def write_to_file(file, new_dictionary, field_name):
    datas = read_data_from_file(file)
    with open(file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        for data in datas:
            writer.writerow(data)
        writer.writerow(new_dictionary)


def save_data_to_file(dictionaries, field_name,  file=QUESTIONS_PATH):
    with open(file, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        for dictionary in dictionaries:
            writer.writerow(dictionary)


def delete_in_file(file, line_to_delete, field_name):
    datas = read_data_from_file(file)
    with open(file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        for data in datas:
            if data["id"] == line_to_delete["id"]:
                if data["image"]:
                    os.remove(f"{STATIC_FOLDER_PATH}/{data['image']}")
                else:
                    pass
            else:
                writer.writerow(data)


def edit_in_file(file, line_to_be_edited, field_name):
    datas = read_data_from_file(file)
    with open(file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        for data in datas:
            if data["id"] == line_to_be_edited["id"]:
                writer.writerow(line_to_be_edited)
            else:
                writer.writerow(data)


def sort_data(list_of_dicts, order_direction, order_by):
    if order_direction == "asc":
        direction = False
    else:
        direction = True
    if order_by == "submission_time":
        sorted_list = sorted(list_of_dicts, key=lambda dicti: dicti[order_by], reverse=direction)
    else:
        numbers = 0
        for dictionary in list_of_dicts:
            if dictionary[order_by].lstrip("-").isnumeric():
                numbers += 1
        if numbers == len(list_of_dicts):
            sorted_list = sorted(list_of_dicts, key=lambda dicti: int(dicti[order_by]), reverse=direction)
        else:
            sorted_list = sorted(list_of_dicts, key=lambda dicti: dicti[order_by].lower(), reverse=direction)
    return sorted_list


def update_vote_number(dictionary, vote):
    number = int((dictionary["vote_number"]))
    if vote == "vote_up":
        number += 1
    elif vote == "vote_down":
        number -= 1
    dictionary["vote_number"] = number
    return dictionary


def save_original_vote_numbers(file_to_save=VOTE_NUMBERS_PATH, file_to_read=QUESTIONS_PATH):
    datas = read_data_from_file(file_to_read)
    dictionaries = []
    for data in datas:
        dictionary = {}
        dictionary["id"] = data["id"]
        dictionary["vote_number"] = data["vote_number"]
        dictionaries.append(dictionary)
    with open(file_to_save, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "vote_number"])
        writer.writeheader()
        for dicti in dictionaries:
            writer.writerow(dicti)


def get_vote_number_from_file(dictionary, file=VOTE_NUMBERS_PATH):
    with open(file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        data = [line for line in reader]
        for elem in data:
            if elem["id"] == dictionary["id"]:
                number = elem["vote_number"]
                return int(number)


def save_new_input(new_data, image, items, answer=False):
    for key, value in items:
        new_data[key] = value
    if image:
        image.save(os.path.join(IMAGE_FOLDER_PATH, image.filename))
        new_data["image"] = f"images/{image.filename}"
    if answer:
        write_to_file(ANSWERS_PATH, new_data, ANSWER_HEADERS_CSV)
    else:
        write_to_file(QUESTIONS_PATH, new_data, QUESTION_HEADERS_CSV)


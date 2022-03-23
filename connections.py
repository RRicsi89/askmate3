import csv
import os
from datetime import datetime


QUESTIONS_PATH = os.getenv('QUESTIONS_PATH') if "QUESTIONS_PATH" in os.environ else "data/questions.csv"
ANSWERS_PATH = os.getenv('ANSWERS_PATH') if "ANSWERS_PATH" in os.environ else "data/answers.csv"
IMAGE_FOLDER_PATH = os.getenv('IMAGE_FOLDER_PATH') if "IMAGE_FOLDER_PATH" in os.environ else "images/"

LIST_HEADERS = ["Submission Time", "Number of views", "Number of votes", "Title", "Message", "Image"]
ANSWER_HEADERS = ["Submission Time", "Vote Number", "Message", "Image"]

QUESTION_HEADERS_CSV = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS_CSV = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


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
    answer_data = read_data_from_file(ANSWERS_PATH)
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

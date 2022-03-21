import csv
import os

QUESTIONS_PATH = os.getenv('QUESTIONS_PATH') if "QUESTIONS_PATH" in os.environ else "data/questions.csv"
ANSWERS_PATH = os.getenv('ANSWERS_PATH') if "ANSWERS_PATH" in os.environ else "data/answers.csv"
LIST_HEADERS = ["Submission Time", "Number of views", "Number of votes", "Title", "Message", "Image"]
ANSWER_HEADERS = ["Submission Time", "Vote Number", "Message", "Image"]


def read_data_from_file(file=None):
    with open(file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return [line for line in reader]


def get_data(data_id, file_to_read_from):
    datas = read_data_from_file(file_to_read_from)
    for data in datas:
        if int(data["id"]) == int(data_id):
            return data

def get_answers_from_file(question_id, file_to_read_from=ANSWERS_PATH):
    answer_data = read_data_from_file(ANSWERS_PATH)
    answers = []
    for data in answer_data:
        if int(data["question_id"]) == int(question_id):
            answers.append(data)
    return answers
            
    
    

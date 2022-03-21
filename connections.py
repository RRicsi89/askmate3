import csv
import os

QUESTIONS_PATH = os.getenv('QUESTIONS_PATH') if "QUESTIONS_PATH" in os.environ else "data/questions.csv"
ANSWERS_PATH = os.getenv('ANSWERS_PATH') if "ANSWERS_PATH" in os.environ else "data/answers.csv"
HEADERS = ["Submission Time", "Number of views", "Number of votes", "Title", "Message", "Image"]


def read_file(file=None):
    with open(file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return [line for line in reader]
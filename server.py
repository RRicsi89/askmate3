from flask import Flask, render_template, request
import connections, data_manager
import datetime

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/list")
def list_questions():
    questions = connections.read_file(connections.QUESTIONS_PATH)
    timestamps = data_manager.convert_timestamps(questions)
    headers = connections.HEADERS
    return render_template("list.html", questions=questions, headers=headers, timestamps=timestamps)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

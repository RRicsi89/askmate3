FROM python:3.12.0a3-alpine3.17
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
COPY . .
ENV FLASK_APP=server.py
EXPOSE 5000
CMD ["flask", "run"]
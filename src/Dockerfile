FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.text ./

RUN pip install -r requirements.text

COPY . .

EXPOSE 4000

CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
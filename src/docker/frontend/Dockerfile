FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

#STARTING WRONG .py File SWITCH TO webClient.py once it is able
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:5001", "webClient:app"]
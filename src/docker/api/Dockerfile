FROM python:3.11-slim-buster

WORKDIR /app

COPY docker/_resources/requirements.txt ./

RUN pip install -r requirements.txt

COPY . .


CMD ["gunicorn", "-w 1", "-b 0.0.0.0:5000", "apiserver:app"]
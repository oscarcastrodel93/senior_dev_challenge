FROM python:3.11

WORKDIR /dev_challenge

COPY ./requirements.txt /dev_challenge/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /dev_challenge/requirements.txt

COPY ./app /dev_challenge/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
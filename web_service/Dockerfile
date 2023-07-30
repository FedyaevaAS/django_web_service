FROM python:3.10-slim-buster

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "web_service.wsgi:application", "--bind", "0:8000"]
FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "collector.py"]

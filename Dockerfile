FROM python:3-slim-buster
ENV PYTHONUNBUFFERED 1
RUN apt update && apt install -y iputils-ping
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
WORKDIR /app
CMD ["python"]

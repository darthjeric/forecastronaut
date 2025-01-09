FROM python:3.9-slim-buster

WORKDIR /app

COPY test_env.py .

CMD ["python", "test_env.py"]
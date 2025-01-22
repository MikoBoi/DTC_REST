FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/infrastructure

RUN mkdir -p htmlcov

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload", "--port", "8000"]
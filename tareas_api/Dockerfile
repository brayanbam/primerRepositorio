FROM python:3.10

WORKDIR /app

# Instalar sqlite3
RUN apt update && apt install -y sqlite3

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5002

CMD ["python", "app.py"]

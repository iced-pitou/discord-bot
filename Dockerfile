FROM python:3.11-alpine

WORKDIR /app
COPY . .

RUN apk add --no-cache build-base
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "-u", "main.py"]

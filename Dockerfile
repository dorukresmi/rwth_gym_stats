FROM python:3.11.6-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Define environment variable
ENV NAME rwth-gym-stats-container

CMD ["python", "main.py"]
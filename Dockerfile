FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY challenges/ ./challenges/
CMD ["python", "-m", "challenges.web_access.app"]

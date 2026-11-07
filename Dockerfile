FROM python:3.12-slim
ENV TZ=Asia/Jakarta PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "etl.main"]

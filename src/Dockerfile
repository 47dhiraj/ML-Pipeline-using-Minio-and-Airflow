FROM python:3.10

ENV MINIO_ACCESS_KEY_ID=your_access_key
ENV MINIO_SECRET_ACCESS_KEY=your_secret_key
ENV MINIO_ENDPOINT=your_minio_endpoint
ENV MINIO_BUCKET_NAME=your_bucket_name

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "model_train_and_publish.py"]
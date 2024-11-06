FROM python:3.9-alpine AS builder

WORKDIR /app

COPY . /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM builder

WORKDIR /build

COPY --from=builder /app /build

EXPOSE 5000

CMD ["python", "app.py"]

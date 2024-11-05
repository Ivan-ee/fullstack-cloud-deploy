FROM python:3.9-slim AS builder

WORKDIR /app

COPY . /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.mirrors.ustc.edu.cn/simple/

#RUN python -m unittest

FROM builder

WORKDIR /build

COPY --from=builder /app /build

EXPOSE 5000

CMD ["python", "app.py"]

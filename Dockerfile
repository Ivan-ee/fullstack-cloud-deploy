FROM python:3.9-slim AS builder

WORKDIR /app

# Установка pipenv
RUN pip install --no-cache-dir pipenv

# Копирование requirements.txt и создание Pipfile на его основе
COPY requirements.txt .

# Создание Pipfile.lock и установка зависимостей
RUN pipenv install --requirements requirements.txt

# Копирование всех файлов приложения
COPY . /app

# Установка рабочей директории
WORKDIR /app

# Установка команды запуска через pipenv
CMD ["pipenv", "run", "python", "app.py"]

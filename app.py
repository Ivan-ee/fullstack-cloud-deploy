import logging
import os

from flask import Flask, request, jsonify
from logging.handlers import SocketHandler
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)

logstash_handler = SocketHandler('logstash', 5000)  # Host и порт Logstash
logstash_handler.setLevel(logging.INFO)

# Формат логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logstash_handler.setFormatter(formatter)

# Добавление логгера
app.logger.addHandler(logstash_handler)
app.logger.setLevel(logging.INFO)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT', 5432)}/{os.getenv('POSTGRES_DB')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = os.getenv("REDIS_HOST")
app.config['CACHE_REDIS_PORT'] = os.getenv("REDIS_PORT", 6379)
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = f"redis://{app.config['CACHE_REDIS_HOST']}:{app.config['CACHE_REDIS_PORT']}/0"

cache = Cache(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

metrics = PrometheusMetrics(app)
metrics.info("app_info", "App Info, this can be anything you want", version="1.0.0")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/data")
@cache.cached(timeout=20)
def get_data():
    return jsonify({"data": "This is the data"})


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(username=data["username"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'})


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()

    user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]

    return jsonify({'users': user_list})


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()

    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User does not exist'}), 404

    user.username = data["username"]
    user.email = data["email"]

    db.session.commit()

    return jsonify({'message': 'User updated successfully'})


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User does not exist'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})


@app.route("/users/<int:id>", methods=["GET"])
@cache.cached(timeout=120, key_prefix="user_data")
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User does not exist'}), 404

    user_data = {'id': user.id, 'username': user.username, 'email': user.email}
    return jsonify(user_data)


@app.route("/clean_cache/<int:id>")
def clean_cache(id):
    cache.delete(f"user_data::{id}")

    return jsonify({'message': f'Cache for user {id} cleared'})


@app.route('/')
def hello_world():
    app.logger.info('Главная страница.')
    return 'Hello, Docker!'


@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

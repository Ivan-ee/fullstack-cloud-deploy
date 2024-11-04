from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@db:5432/cloud_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


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


@app.route('/')
def hello_world():
    app.logger.info('Главная страница.')
    return 'Hello, Docker!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')

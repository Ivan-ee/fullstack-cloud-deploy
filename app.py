from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    app.logger.info('Главная страница.')
    return 'Hello, Docker!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')

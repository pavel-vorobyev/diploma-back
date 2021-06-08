from flask import Flask
from db import guard, visit, visitor

app = Flask(__name__)


@app.route('/subsystem/lock/register')
def lock_register():
    return 'Hello World!'


@app.route("/subsystem/lock/verify")
def lock_verify():
    return 'Hello World'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9173)

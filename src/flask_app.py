from flask import Flask

print('\nflask_app - creating an instance of the flask library')
flask_app = Flask(__name__)

# test flask app
@flask_app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
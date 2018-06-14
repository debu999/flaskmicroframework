"""Flask microframework viola lets code"""

from flask import Flask

application = Flask(__name__)

@application.route("/")
@application.route("/index")
def index():
    return "Hello World in Flask WORLD!!!!!"

@application.route("/about")
def about():
    return "This app must be run via gunicorn and served by the wsgi http server.cd "


if __name__ == "__main__":
    application.run()

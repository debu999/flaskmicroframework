"""Flask microframework thermos module viola lets code"""

from flask import Flask, render_template, url_for

application = Flask(__name__)

@application.route("/")
@application.route("/index")
def index():
    # return "Hello World in Flask WORLD!!!!!"
    return render_template("index.html")

@application.route("/about")
def about():
    return "This app must be run via gunicorn and served by the wsgi http server.cd "


if __name__ == "__main__":
    application.run(debug=True)

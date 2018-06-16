"""Flask microframework thermos module viola lets code"""
import sys, os
from pprint import pprint as pp
import logging
from logging import Formatter, FileHandler

from flask import Flask, render_template, url_for, request, redirect, flash
from datetime import datetime
from logging import DEBUG
from thermos.users import User
from thermos.thermoscrypto.cryptostringgen import id_generator
from thermos.forms import BoookmarkForm

application = Flask(__name__)
# application.config['DEBUG'] = True
application.config["SECRET_KEY"] = id_generator(24)
application.logger.setLevel(DEBUG)
bookmarks = []


def storebookmark(url, user="Debarbrata", description=""):
    bookmarks.append(dict(url=url, user=user or "Debabrata",
                          description=description, date=datetime.now()))


def newbookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


@application.route("/")
@application.route("/index")
def index():
    # return "Hello World in Flask WORLD!!!!!"
    application.logger.debug('this is a DEBUG message')
    application.logger.info('this is an INFO message')
    application.logger.warning('this is a WARNING message')
    application.logger.error('this is an ERROR message')
    application.logger.critical('this is a CRITICAL message')
    application.logger.info('Route to /index')
    application.logger.debug('reroute from root to /index')
    return render_template("index.html", title="Title Passed from View to Template",
                           text="Sample text for the Web Application.",
                           user=User("Debabrata", "Patnaik"), newbookmarks=newbookmarks(5))


@application.route("/add", methods=["GET", "POST"])
def add():
    form = BoookmarkForm()
    application.logger.info('Route to /add')
    application.logger.debug('no reroute from root to /add')
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        user = form.user.data
        application.logger.info(url, description, user)
        storebookmark(url, user, description)

        # if request.method == "POST":
        #     url = request.form.get("url")
        #     user = request.form.get("user")
        #     storebookmark(url, user)
        application.logger.info("Added url for user url: {}, user: {}".format(url, user or "Debabrata"))
        flash("Bookmarked url: {} for user: {}".format(url, user if user else "Debabrata(Default)"))
        return redirect(url_for("index"))

    return render_template("add.html", form=form)


@application.route("/about")
def about():
    return "This app must be run via gunicorn and served by the wsgi http server.cd "


@application.errorhandler(404)
def pagenotfound(e):
    return render_template("404.html"), 404


@application.errorhandler(500)
def servererror(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    application.run(debug=True)

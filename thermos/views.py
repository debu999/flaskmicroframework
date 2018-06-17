"""Flask microframework thermos module viola lets code"""

from flask import render_template, url_for, request, redirect, flash, abort
from thermos import application, db, login_manager
from datetime import datetime

from thermos.users import Userobj
from thermos.forms import BookmarkForm, LoginForm, SignupForm
from thermos.models import Bookmark, User, Tag
from flask_login import login_required, login_user, logout_user, current_user
bookmarks = []


def storebookmark(url, user="Debabrata", description=""):
    bookmarks.append(dict(url=url, user=user or "Debabrata",
                          description=description or url, date=datetime.now()))


def newbookmarks(num):
    # return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]
    return Bookmark.newbookmarks(num=num)

# Fake Login
def admin_user():
    return User.query.filter_by(username="Debabrata").first()

@application.route("/")
@application.route("/index")
@login_required
def index():
    # return "Hello World in Flask WORLD!!!!!"
    application.logger.info('Route to /index via root')
    # return render_template("index.html", title="Title Passed from View to Template",
    #                        text="Sample text for the Web Application.",
    #                        user=Userobj("Debabrata", "Patnaik"), newbookmarks=newbookmarks(5))

    return render_template("index.html", title="Title Passed from View to Template",
                    text="Sample text for the Web Application.",
                    user=current_user, newbookmarks=Bookmark.newbookmarks(5))

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@application.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = BookmarkForm()
    application.logger.info('Route to /add')
    application.logger.debug('no reroute from root to /add')
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        user = form.user.data
        application.logger.info(str(url), str(description), str(user))
        print(db.session)
        bkusr = User.query.filter_by(username=user).first()
        if not bkusr and user:
            bkusr = User(username=user, email=user+"@thermos.com")
            db.session.add(bkusr)
        tags = form.tags.data
        bkm = Bookmark(url=url, description=description, user=bkusr or current_user, bkmrkusername=bkusr.username,
                       tags=tags)
        db.session.add(bkm)
        db.session.commit()
        storebookmark(url, user, description)
        # if request.method == "POST":
        #     url = request.form.get("url")
        #     user = request.form.get("user")
        #     storebookmark(url, user)
        application.logger.info("Added url for user url: {}, user: {}".format(url, user or "Debabrata"))
        flash("Bookmarked url: {} for user: {}".format(url, user if user else "Debabrata(Default)"))
        return redirect(url_for("index"))
    return render_template("bookmarkform.html", form=form)


@application.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    application.logger.info("found user {}".format(user.username))
    return render_template("user.html", user=user)

@application.route("/about")
def about():
    return "This app must be run via gunicorn and served by the wsgi http server.cd "


@application.errorhandler(404)
def pagenotfound(e):
    return render_template("404.html"), 404


@application.errorhandler(500)
def servererror(e):
    return render_template("500.html"), 500


@application.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        #login and validate useer:
        user = User.getuserbyusername(username=form.username.data)
        if user is not None and user._checkpassword(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in Successfully as {}".format(user.username))
            return redirect(request.args.get('next') or url_for("user", username=user.username))
        flash("Incorrect User Details entered or User Not found. Please try again or signup.")

    return render_template("login.html", form=form)

@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@application.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Welcome {} to Thermos App. Please login now to your account.".format(user.username))
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@application.route("/edit/<int:bookmark_id>", methods=["GET", "POST"])
@login_required
def editbookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)

    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Stored '{}' with updates".format(bookmark.description))
        return redirect(url_for("user", username=current_user.username))
    return render_template("bookmarkform.html", form=form, title="{}: Edit Bookmark".format(current_user.username))


if __name__ == "__main__":
    application.run(debug=True)

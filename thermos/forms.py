from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Regexp, EqualTo, Email, ValidationError

from thermos.models import User


class BookmarkForm(FlaskForm):
    # url = URLField("url", validators=[DataRequired(), url()])
    # description = StringField('description')
    # user = StringField('user')

    url = URLField("Enter your bookmark here: ", validators=[DataRequired(), url()])
    description = StringField('Enter URL description(optional) here: ', validators=[Length(5, 100)])
    user = StringField('Enter your username here: ')
    tags = StringField("Tags", validators=[Regexp(r"[a-zA-Z0-9, ]*$",
                                            message="Tags can contain only number and letters(comma separated)")])

    def validate(self):
        if not self.url.data.startswith((r"http://", r"https://")):
            self.url.data = "".join(["https://",self.url.data])

        if not FlaskForm.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        if not self.user.data:
            self.user.data = current_user.username

        # filter out the tags from the system
        stripped = set(filter(None, [t.strip() for t in self.tags.data.split(",")]))
        self.tags.data=",".join(sorted(stripped))

        return True


class LoginForm(FlaskForm):
    username = StringField("Your Username:", validators=[DataRequired(),])
    password = PasswordField("Password:", validators=[DataRequired(), ])
    remember_me = BooleanField("Keep Me Logged In")
    submit = SubmitField("Log In")


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(3, 16),
                                                   Regexp("^[A-Za-z0-9_]{3,}$",
                                                          message="Username can contain letters, digits and _")
                                                   ])

    password = PasswordField("Password", validators=[DataRequired(),
                                                   EqualTo("password2", message="Password must match. Please retype password."),
                                                   ])

    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Length(1,50), Email()])
    submit = SubmitField("SignUp")

    def validate_email(self, emailfield):
        if User.query.filter_by(email=emailfield.data).first():
            raise ValidationError("There is already a user with given email. If you have forgotten password, please reset.")


    def validate_username(self, usernamefield):
        if User.query.filter_by(username=usernamefield.data).first():
            raise ValidationError("This username is already taken.")




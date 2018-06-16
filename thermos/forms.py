from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url

class BoookmarkForm(FlaskForm):
    # url = URLField("url", validators=[DataRequired(), url()])
    # description = StringField('description')
    # user = StringField('user')

    url = URLField("Enter your bookmark here: ", validators=[DataRequired(), url()])
    description = StringField('Enter URL description(optional) here: ')
    user = StringField('Enter your username here: ')

    def validate(self):
        if not self.url.data.startswith((r"http://", r"https://")):
            self.url.data = "".join(["https://",self.url.data])

        if not FlaskForm.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        if not self.user.data:
            self.user.data = "Debabrata Patnaik"

        return True
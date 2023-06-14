from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, Length

app = Flask(__name__)

app.secret_key = "somesecretstring"


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email(check_deliverability=True)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, message=None)])
    submit = SubmitField(label='Login')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():

    return render_template("login.html", form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
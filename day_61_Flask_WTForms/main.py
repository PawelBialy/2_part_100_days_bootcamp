from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, Length
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
app.secret_key = "somesecretstring"

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email(check_deliverability=True)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, message=None)])
    submit = SubmitField(label='Login')


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/button", methods=["POST"])
def button():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "!" and login_form.password.data == "123456789" :
            return  render_template("success.html")
        else :
            return render_template('denied.html')
    return render_template("login.html", form=login_form)


if __name__ == '__main__':
    app.run(debug=True)

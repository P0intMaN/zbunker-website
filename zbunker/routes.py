from logging import exception
from wtforms.validators import ValidationError
from zbunker import app, db, mail
from flask_mail import Message
from flask import render_template, redirect, flash, url_for, request, jsonify, session
from zbunker.forms import (
    LoginForm,
    RegistrationForm,
    OTPForm,
    ResetPasswordForm,
    VerifyOTPForm,
)
from zbunker.models import User, OTPModel
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required
import json
import re
from random import randint
import os


@app.route("/")
def landing():
    return render_template("landing.html", title="Landing")


@app.route("/home")
def home():
    videos = [1, 2, 3, 4, 5, 6, 7]
    return render_template("home.html", videos=videos)


@app.route("/prime", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            return render_template(
                "prime.html", anchor=1, title="Join Prime", form=form
            )

    return render_template("prime.html", title="Join Prime", form=form)
    # return redirect(url_for('register', _anchor='prime-anchor'))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remMe.data)
            nextPage = request.args.get(
                "next"
            )  # a feature to route to the next url (for login_required only)
            if not nextPage or url_parse(nextPage).netloc != "":
                nextPage = url_for("home")

            return redirect(nextPage)

        else:
            flash(
                "Login Unsuccessful. Please check email and password", category="danger"
            )

    return render_template("login.html", form=form)


# Email Validation Route
@app.route("/forgot-password", methods=["GET", "POST"])
def forgotpassword():
    form = OTPForm()

    if request.method == "POST":

        if form.validate_on_submit():
            email = User.query.filter_by(email=form.email.data).first()
            if email:
                otp = gen_otp()  # Generate OTP
                new_otp = OTPModel(email=form.email.data, otp=otp)
                db.session.add(new_otp)
                db.session.commit()
                msg = Message(
                    sender=os.environ.get("EMAIL_ADDRESS"),
                    recipients=[form.email.data],
                    subject="Forgot Password | ZBunker",
                )
                msg.html = render_template("forgot_password_email.html", otp=otp)
                try:
                    mail.send(msg)

                except Exception as e:
                    print(e)
                    flash(
                        "Something went wrong while sending the OTP.", category="danger"
                    )
            session["user_email"] = form.email.data

            return redirect(url_for("otpverify"))

    return render_template("forgot-password.html", form=form)


def gen_otp():
    keybase = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    otp = ""
    for i in range(6):
        otp += str(keybase[randint(0, len(keybase) - 1)])
    print(otp)
    return otp


@app.route("/validate/otp", methods=["GET", "POST"])
def otpverify():
    form = VerifyOTPForm()
    try:
        email = session["user_email"]
    except:
        email = None

    if request.method == "POST":
        if form.validate_on_submit():
            if email:
                user = (
                    OTPModel.query.filter_by(email=email)
                    .order_by(OTPModel.id.desc())
                    .first()
                )

                if user.otp != form.OTP.data:
                    flash("Your Password is Incorrect. Try Again")

                else:
                    return redirect(url_for("resetpassword"))

    return render_template("enter-otp.html", form=form)


@app.route("/reset-password", methods=["GET", "POST"])
def resetpassword():
    try:
        email = session["user_email"]
    except:
        email = None
    form = ResetPasswordForm()

    if request.method == "POST":
        if form.validate_on_submit():
            if email:
                user = User.query.filter_by(email=email).first()
                if user:
                    user.set_password(form.password.data)
                    db.session.commit()
                    return redirect(url_for("home"))

                else:
                    flash("something doesn't seem right (UDE)", category="danger")

            else:
                flash("Something doesn't seem right. (SESSNONE)", category="danger")

    return render_template("reset-password.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/pt")
def pt():
    form = RegistrationForm()
    return render_template("pt.html", form=form)


@app.route("/about")
def about():
    title = "About"
    return render_template("about.html", title=title)


@app.route("/basic")
def basic():
    title = "Basic"
    return render_template("basic.html", title=title)


@app.route("/learn")  # change this
def filter():
    title = "Filter"
    return render_template("filtergrid.html", title=title)


@app.route("/support-zbunker")
@app.route("/donate")
def zbunkerprime():
    title = "Support Us"

    # get the no of users and calc the percentage (short goal)
    user = User.query.all()
    total = 20  #  the target goal
    members = len(user)
    percentage = (members / total) * 100
    filler = str(percentage) + "%"
    marker = 86.5

    if percentage > 100:
        marker = "0%"
    else:
        if 100 - percentage < 86.5:
            marker = str(100 - percentage) + "%"
        else:
            marker = str(86.5) + "%"

    return render_template(
        "donate.html",
        title=title,
        members=members,
        filler=filler,
        marker=marker,
        total=total,
    )


@app.route("/sponsors")
def sponsor():
    title = "Sponsors"

    users = User.query.all()
    sponsors = []

    for user in users:
        sponsors.append(user.username)

    return render_template("sponsors.html", title=title, sponsors=sponsors)


@app.route("/learn/ethical-hacking")
def eth():
    title = "Ethical Hacking"
    return render_template("eth.html", title=title)


@app.route("/learn/python-programming")
def pythonprogramming():
    title = "Python Programming"
    return render_template("python.html", title=title)


@app.route("/learn/git-essentials")
def git():
    title = "Git Essentials"
    return render_template("git.html", title=title)


@app.route("/learn/nmap")
def nmap():
    title = "Nmap"
    return render_template("nmap.html", title=title)


@app.route("/learn/mongodb")
def mongo():
    title = "Mongo DB"
    return render_template("mongo.html", title=title)


@app.route("/learn/linux-essentials")
def linux():
    title = "Linux"
    return render_template("linux.html", title=title)


@app.route("/learn/c-programming")
def c():
    title = "C Programming"
    return render_template("c.html", title=title)


@app.route("/learn/postgresql")
def postgres():
    title = "Learn PostgreSQL"
    return render_template("postgres.html", title=title)


@app.route("/contact-us")
def contact():

    title = "Contact Us"
    return render_template("contact.html", title=title)

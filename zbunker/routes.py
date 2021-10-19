from zbunker import app, db, mail
from flask_mail import Message
from flask import render_template, redirect, flash, url_for, request, jsonify
from zbunker.forms import LoginForm, RegistrationForm
from zbunker.models import User, OTPModel
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
            user = User(
                username=form.username.data,
                email=form.email.data
            )
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
            return redirect(nextPage) if nextPage else redirect(url_for("home"))

        else:
            flash(
                "Login Unsuccessful. Please check email and password", category="danger"
            )

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

# Email Validation Route
@app.route('/validate/email', methods=['POST'])
def email_validation():
    data = json.loads(request.data)
    email = data['email']
    pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if not bool(re.match(pattern, email)):
        return jsonify(email_error='Please enter a valid email address.')
    return jsonify(email_valid=True)

def gen_otp():
    return randint(100000, 999999)

@app.route("/validate/send-otp", methods=["GET"])
def send_otp():
    user_email = request.args.get('email')
    if User.query.filter_by(email=user_email).first():
        otp = gen_otp()     # Generate OTP
        new_otp = OTPModel(email=user_email,otp=otp)
        db.session.add(new_otp)
        db.session.commit()
        msg = Message(sender=os.environ.get('EMAIL_ADDRESS'), recipients=[user_email], subject='Forgot Password | ZBunker')
        msg.html = render_template('forgot_password_email.html', otp=otp)
        try:
            mail.send(msg)
            return jsonify(otp_sent=f'An OTP has been sent successfully to {user_email}')
        except Exception as e:
            print(e)
            return jsonify(otp_error='Something went wrong while sending the OTP.')
    return jsonify(user_not_found=True)

@app.route("/validate/verify-otp", methods=["GET"])
def validate_otp():
    user_email = request.args.get('email')
    otp = request.args.get('otp')
    otp_from_db = OTPModel.query.filter_by(email=user_email).order_by(OTPModel.id.desc()).first()
    if str(otp_from_db.otp) == str(otp):
        return jsonify(otp_match=True)
    return jsonify(otp_mismatch='Please enter the correct OTP')


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Your password has been changed successfully!', category='success')
        return redirect(url_for('login'))

    return render_template("forgot-password.html")


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

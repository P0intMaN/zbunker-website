from zbunker import app, db, mail
from flask_mail import Message
from flask import render_template, redirect, flash, url_for, request, jsonify
from zbunker.forms import LoginForm, RegistrationForm
from zbunker.models import User, OTPModel
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required
import json
import re
from random import randint
import os
import stripe


STRIPE_KEYS = {
    "secret_key": os.environ.get("STRIPE_SECRET_KEY"),
    "publishable_key": os.environ.get("STRIPE_PUBLISHABLE_KEY"),
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
}

stripe.api_key = STRIPE_KEYS["secret_key"]


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
            flash('Signup success, please log in')
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
            else:
                # Redirect to payments page
                nextPage = url_for("payment")
            
            return redirect(nextPage)

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
@app.route("/validate/email", methods=["POST"])
def email_validation():
    data = json.loads(request.data)
    email = data["email"]
    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not bool(re.match(pattern, email)):
        return jsonify(email_error="Please enter a valid email address.")
    return jsonify(email_valid=True)


def gen_otp():
    return randint(100000, 999999)


@app.route("/validate/send-otp", methods=["GET"])
def send_otp():
    user_email = request.args.get("email")
    if User.query.filter_by(email=user_email).first():
        otp = gen_otp()  # Generate OTP
        new_otp = OTPModel(email=user_email, otp=otp)
        db.session.add(new_otp)
        db.session.commit()
        msg = Message(
            sender=os.environ.get("EMAIL_ADDRESS"),
            recipients=[user_email],
            subject="Forgot Password | ZBunker",
        )
        msg.html = render_template("forgot_password_email.html", otp=otp)
        try:
            mail.send(msg)
            return jsonify(
                otp_sent=f"An OTP has been sent successfully to {user_email}"
            )
        except Exception as e:
            print(e)
            return jsonify(otp_error="Something went wrong while sending the OTP.")
    return jsonify(user_not_found=True)


@app.route("/validate/verify-otp", methods=["GET"])
def validate_otp():
    user_email = request.args.get("email")
    otp = request.args.get("otp")
    otp_from_db = (
        OTPModel.query.filter_by(email=user_email).order_by(OTPModel.id.desc()).first()
    )
    if str(otp_from_db.otp) == str(otp):
        return jsonify(otp_match=True)
    return jsonify(otp_mismatch="Please enter the correct OTP")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Your password has been changed successfully!", category="success")
        return redirect(url_for("login"))

    return render_template("forgot-password.html")

@app.route('/payment')
def payment():
    """Payment Route - Accessible only to logged in users"""

    if current_user.is_authenticated:
        if current_user.prime:
            return redirect('home')
        return render_template('payment.html')
    flash('You are not logged in!', category='error')
    return redirect('login')

@app.route("/config")
def get_publishable_key():
    """Route to get the publishable_key on the client side"""
    
    stripe_config = {"publicKey": STRIPE_KEYS["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session")
def create_checkout_session():
    """Route to create checkout session"""
    
    if current_user.is_authenticated:
        domain_url = os.environ.get("DOMAIN_URL")
        stripe.api_key = STRIPE_KEYS["secret_key"]

        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                customer_email=current_user.email,
                client_reference_id=current_user.id if current_user.is_authenticated else None,
                success_url=domain_url +
                "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "name": "Prime Subscription",
                        "quantity": 1,
                        "currency": "inr", # TODO: Change the currency
                        "amount": "30000", # TODO: Change the amount
                    }
                ]
            )
            return jsonify({"sessionId": checkout_session["id"]})
        except Exception as e:
            print(e)
            return jsonify(error=str(e)), 403
    flash('You are not logged in!', category='error')
    return redirect('login')


@app.route("/success")
def success():
    """Route to show payment success message"""
    if current_user.is_authenticated:
        if current_user.prime:
            return render_template("success.html", header='Payment Success', para='Thanks for your support.')
        return render_template("success.html", header='Access Denied', para='Please login again to pay!')
    flash('You are not logged in!', category='error')
    return redirect('login')

@app.route("/cancelled")
def cancelled():
    """Route for failed payment message"""
    if current_user.is_authenticated:
        if not current_user.prime:
            return render_template("cancelled.html")    
        return redirect('home')
    flash('You are not logged in!', category='error')
    return redirect('login')


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    """Route to confirm payment using Webhook - called by Stripe automatically"""
    
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_KEYS["endpoint_secret"]
        )

    except ValueError:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
    
        # On Payment success, set the prime field to true
        user_id = event["data"]["object"]["client_reference_id"]
        user = User.query.filter_by(id=user_id).first()
        user.prime = True
        db.session.add(user)
        db.session.commit()


    return "Success", 200


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
    total = 20  # the target goal
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

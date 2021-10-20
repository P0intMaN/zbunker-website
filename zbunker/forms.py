from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from zbunker.models import OTPModel, User
from flask import session


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=30)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPassword = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username / Email already exists. Try logging in.")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Username / Email already exists. Try logging in.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remMe = BooleanField("Remember Me")
    login = SubmitField("Login")


class OTPForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    sendOTP = SubmitField("SEND OTP")


class VerifyOTPForm(FlaskForm):
    OTP = StringField("OTP")
    verifyOTP = SubmitField("Verify")

    def validate_OTP(self, OTP):
        user = (
            OTPModel.query.filter_by(email=session["user_email"])
            .order_by(OTPModel.id.desc())
            .first()
        )
        if user:
            if user.otp != OTP.data:
                raise ValidationError("Incorrect OTP. Try Again")
        else:
            raise ValidationError("Incorrect OTP. Try Again!")


class ResetPasswordForm(FlaskForm):
    password = StringField("New Password", validators=[DataRequired()])
    confirmpass = StringField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    confirm = SubmitField("Confirm")


class NewVideoForm(FlaskForm):
    pass

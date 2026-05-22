# app/auth/routes.py

from flask import Blueprint

# auth views
from .views.register import RegisterAPI
from .views.login import LoginAPI
from .views.me import MeAPI

# password reset views
from .views.forgot_password import ForgotPasswordAPI
from .views.reset_password import ResetPasswordAPI
from .views.request_reset import RequestResetAPI

# oauth views
from .views.google import GoogleAPI
from .views.google_callback import GoogleCallbackAPI

# email verification
from .views.verify_email import VerifyEmailAPI
from .views.resend_code import ResendCodeAPI

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# Authentication
auth_bp.add_url_rule("/register", view_func=RegisterAPI.as_view("register"))
auth_bp.add_url_rule("/login", view_func=LoginAPI.as_view("login"))
auth_bp.add_url_rule("/me", view_func=MeAPI.as_view("me"))


# Password reset
auth_bp.add_url_rule(
    "/forgot-password",
    view_func=ForgotPasswordAPI.as_view("forgot_password")
)

auth_bp.add_url_rule(
    "/reset-password",
    view_func=ResetPasswordAPI.as_view("reset_password")
)

auth_bp.add_url_rule(
    "/request-reset",
    view_func=RequestResetAPI.as_view("request_reset")
)


# Google OAuth
auth_bp.add_url_rule(
    "/google",
    view_func=GoogleAPI.as_view("google")
)

auth_bp.add_url_rule(
    "/google/callback",
    view_func=GoogleCallbackAPI.as_view("google_callback")
)

# Email Verification
auth_bp.add_url_rule(
    "/verify-email",
    view_func=VerifyEmailAPI.as_view("verify_email")
)

auth_bp.add_url_rule(
    "/resend-code",
    view_func=ResendCodeAPI.as_view("resend_code")
)
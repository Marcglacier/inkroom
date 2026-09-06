# app/auth/routes.py

from flask import Blueprint

# auth views
from .views.registration import (
    RegisterAPI,
    VerifyRegistrationAPI,
)
from .views.login import LoginAPI
from .views.me import MeAPI

# password reset views
from .views.forgot_password import ForgotPasswordAPI
from .views.reset_password import ResetPasswordAPI
from .views.request_reset import RequestResetAPI

# Google OAuth
from .views.google.google import GoogleAPI
from .views.google.google_callback import GoogleCallbackAPI
from .views.google.google_complete import GoogleCompleteAPI

# Email verification
from .views.resend_code import ResendCodeAPI


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth",
)


# ==========================================================
# AUTHENTICATION
# ==========================================================

auth_bp.add_url_rule(
    "/register",
    view_func=RegisterAPI.as_view("register"),
)

auth_bp.add_url_rule(
    "/register/verify",
    view_func=VerifyRegistrationAPI.as_view(
        "verify_registration"
    ),
    methods=["POST"],
)

auth_bp.add_url_rule(
    "/login",
    view_func=LoginAPI.as_view("login"),
)

auth_bp.add_url_rule(
    "/me",
    view_func=MeAPI.as_view("me"),
)


# ==========================================================
# PASSWORD RESET
# ==========================================================

auth_bp.add_url_rule(
    "/forgot-password",
    view_func=ForgotPasswordAPI.as_view("forgot_password"),
)

auth_bp.add_url_rule(
    "/reset-password",
    view_func=ResetPasswordAPI.as_view("reset_password"),
)

auth_bp.add_url_rule(
    "/request-reset",
    view_func=RequestResetAPI.as_view("request_reset"),
)


# ==========================================================
# GOOGLE OAUTH
# ==========================================================

auth_bp.add_url_rule(
    "/google",
    view_func=GoogleAPI.as_view("google"),
)

auth_bp.add_url_rule(
    "/google/callback",
    view_func=GoogleCallbackAPI.as_view("google_callback"),
)

auth_bp.add_url_rule(
    "/google/complete",
    view_func=GoogleCompleteAPI.as_view("google_complete"),
    methods=["POST"],
)


# ==========================================================
# EMAIL
# ==========================================================

auth_bp.add_url_rule(
    "/resend-code",
    view_func=ResendCodeAPI.as_view("resend_code"),
)
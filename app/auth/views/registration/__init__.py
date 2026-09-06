# views/register.py/__init__.py
from .register import RegisterAPI
from .verify import VerifyRegistrationAPI


__all__= [
    "RegisterAPI",
    "VerifyRegistrationAPI"
]
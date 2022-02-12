from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import email, forms, routes  # noqa: E402, F401

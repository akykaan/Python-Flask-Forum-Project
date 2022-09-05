from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('error',__name__)

@bp.errorhandler(403)
def access_denied(e):
    return render_template('error/error.html'),403
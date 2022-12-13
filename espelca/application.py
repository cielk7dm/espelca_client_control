from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from espelca.auth import login_required
from espelca.db import get_db

bp = Blueprint('application', __name__)

@bp.route('/')
def index():
    return render_template('client/index.html', )

@bp.route('/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    return render_template('client/dashboard.html')

@bp.route('/payments', methods=('GET', 'POST'))
@login_required
def payments():
    return render_template('client/payments.html')

@bp.route('/clients', methods=('GET', 'POST'))
@login_required
def clients():
    return render_template('client/clients.html')

@bp.route('/slots', methods=('GET', 'POST'))
@login_required
def slots():
    return render_template('client/slots.html')

@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    return render_template('client/settings.html')
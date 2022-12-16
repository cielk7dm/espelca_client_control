from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from espelca.auth import login_required
from espelca.db import get_db
import socket
bp = Blueprint('application', __name__)

@bp.route('/')
def index():
    hostname = socket.gethostname()
    return render_template('client/index.html', hostname=hostname)

@bp.route('/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    hostname = socket.gethostname()
    return render_template('client/dashboard.html', hostname=hostname)

@bp.route('/payments', methods=('GET', 'POST'))
@login_required
def payments():
    hostname = socket.gethostname()
    return render_template('client/payments.html', hostname=hostname)

@bp.route('/clients', methods=('GET', 'POST'))
@login_required
def clients():
    hostname = socket.gethostname()
    return render_template('client/clients.html', hostname=hostname)

@bp.route('/slots', methods=('GET', 'POST'))
@login_required
def slots():
    hostname = socket.gethostname()
    return render_template('client/slots.html', hostname=hostname)

@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    hostname = socket.gethostname()
    return render_template('client/settings.html', hostname=hostname)
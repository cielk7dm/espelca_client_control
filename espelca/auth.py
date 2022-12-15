import functools
import datetime
from flask import(Blueprint, flash, g, redirect, render_template, request,session,url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from espelca.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password =  request.form['password']
        checkbox = request.form.getlist('checkbox')
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        
        if error is None:
            try:
                db.execute("INSERT INTO user (username, password, isadmin) VALUES (?,?,?)",
                 (username, generate_password_hash(password), bool(checkbox)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        
        user = db.execute('SELECT * FROM user WHERE username =  ?', (username,)).fetchone()
        if user is None:
            error = 'Username not found'
        elif not check_password_hash(user['password'], password):
            error = 'Password is incorrect'
        
        if error is None:
            session.clear()
            user_session = db.execute("SELECT * FROM user_session WHERE user_id=? AND isclosed =0",
            (user['id'],)).fetchone()
            
            if user_session is None:
                print('2paso')
                try:
                    db.execute("INSERT INTO user_session(user_id) VALUES(?)", (user['id'],)
                    )
                    db.commit()
                    session['user_id'] = user['id']
                except db.IntegrityError:
                    error = f"User_session for {username} has error."
            elif user_session['isclosed'] == 0:
                session['user_id'] = user_session['user_id']
            
            return redirect(url_for('index'))

        flash(error)
    return render_template('/auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    print(len(session))
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE user.id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    db = get_db()
    error = None
    user_session = db.execute("SELECT * FROM user_session WHERE user_id=? AND isclosed = 0", (session['user_id'],)
    ).fetchone()
    if user_session is None:
        error = 'user_session not found.'
    if error is None:
        try:
            db.execute("UPDATE user_session SET finished=?, isclosed=1 WHERE user_id=? AND isclosed=0", 
            (datetime.datetime.now(), session['user_id'],)
            )
            db.commit()
        except db.IntegrityError:
            error = 'Uodating user_session has an error.'
        session.clear()
    
    flash(error)
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
                return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view
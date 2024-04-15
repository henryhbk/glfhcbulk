# @author: Henry Feldman MD
# (c) 2024 Greater Lawrence Family Health Center
# All Rights Reserved

import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

blueprint = Blueprint('auth', __name__)


@blueprint.route('/logout')
def logout():
    """
    Logout the user by clearing the session.

    :return: Redirects to the 'index' route.
    """
    session.clear()
    return redirect(url_for('index'))


@blueprint.before_app_request
def load_logged_in_user():
    """
    Load the currently logged in user information.

    :return: None
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    """

    Register

    This method handles the registration functionality. It checks if the request method is POST, retrieves the username and password from the form data, and performs validation checks. If there are no validation errors, it inserts the user data into the database and redirects the user to the login page. If there are validation errors, it displays an error message using flash and renders the registration template.

    :return: None

    """
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'

       #if error is None:
            # try:
            #     db.execute(
            #         "INSERT INTO user (username) VALUES (?)",
            #         (username, generate_password_hash(password)),
            #     )
            #     db.commit()
            # except db.IntegrityError:
            #     error = f"User {username} is already registered."
            # else:
            #     return redirect(url_for("auth.login"))

        #flash(error)

    return render_template('register.html')


@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    """
    Login method for the authentication route '/login', which supports GET and POST requests.

    :return: None
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


def login_required(view):
    """
    Requires the user to be logged in to access a specific view.

    :param view: The view function to be checked for login requirement.
    :return: The wrapped view function that redirects to the login page if the user is not logged in.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
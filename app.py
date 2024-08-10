from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "your_secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Redirect to the list of users."""
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    """List all users."""
    users = User.query.all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET", "POST"])
def add_user():
    """Show form to add a new user and process the form."""
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form.get('image_url') or None

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        flash(f"User {new_user.full_name} added.")
        return redirect(url_for('list_users'))

    return render_template('users/new.html')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details of a single user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Show form to edit a user and process the form."""
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form.get('image_url') or None

        db.session.commit()
        flash(f"User {user.full_name} updated.")
        return redirect(url_for('list_users'))

    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.full_name} deleted.")
    return redirect(url_for('list_users'))

if __name__ == "__main__":
    app.run(debug=True)

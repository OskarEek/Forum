from flask import render_template, request, jsonify, Flask, flash, redirect, url_for, current_app
from .. import db
from . import main
from ..models import Item, User
from .forms import AddItemForm, RegisterUserForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)



@main.route('/', methods = ['GET', 'POST'])  # METHOD
@login_required
def index():
    """Default application route."""

    #  FORM
    form = AddItemForm()
    if form.validate_on_submit():
        item = Item(title=form.title.data, description=form.description.data, author=current_user)
        db.session.add(item)
        db.session.commit()

    items = db.session.query(Item).filter_by(done=False).all()
    return render_template('index.html', items=items, form = form)  # form=form


@main.route("/update", methods=['POST'])
def update():
    """Update item state."""
    json = request.get_json()
    item = db.session.query(Item).filter_by(id=json['itemId']).first()
    if item:

        print(json)
        #checkbox_value = db.session.query(Item).filter_by(id=json['itemDone']).first()
        item.done = not item.done
        db.session.commit()
        # if item.done == True:
        #     db.session.delete(item)
        #     db.session.commit()
        #     print('about to delete' + item)
        # return redirect('http://localhost:5000')
        #return render_template('index.html', item=item)
        return jsonify({'status': 'ok', 'itemId': item.id})
    return jsonify({'status': 'error'}), 400  # Return with status 400

@main.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for regestering')
        return redirect(url_for('main.login'))
    return render_template('register.html', form = form)

logger.info

@main.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        current_app.logger.info(db.session.query(User).filter_by(username = User.username).all())
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

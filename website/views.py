from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from website.models import Games
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        score = request.form.get('score')

        game = Games.query.filter_by(name=name).first()

        if game:
            flash('The game is already exists', category='error')
        else:
            new_game = Games(
                name=name,
                price=price,
                description=description,
                score=score,
                user_id=current_user.id
            )
            db.session.add(new_game)
            db.session.commit()
            print("NEW GAME ADDED")
            # login_user(game, remember=True)
            return redirect(url_for('views.home'))

    return render_template("create.html", user=current_user)

@views.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    game = Games.query.filter_by(id=id).first()

    if request.method == 'POST':
        if game:
            db.session.delete(game)
            db.session.commit()

        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        score = request.form['score']

        game = Games(
            name=name,
            price=price,
            description=description,
            score=score,
            user_id=current_user.id
        )
        db.session.add(game)
        db.session.commit()
        return redirect('/')
        return f"Student with id = {id} Does not exists"

    return render_template('update.html', game=game, user=current_user)

@views.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    game = Games.query.filter_by(id=id).first()

    if game:
        db.session.delete(game)
        db.session.commit()
        return redirect("/")


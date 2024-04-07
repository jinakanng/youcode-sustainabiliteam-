from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from website.models import Entry
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        entry = request.form.get('entry')

        if len(entry) < 1:
            flash('Entry is too short!', category='error')

        else:
            new_entry = Entry(data=entry, user_id=current_user.id)
            db.session.add(new_entry)
            db.session.commit()
            flash('New adventure logged!', category='success')
    return render_template('home.html', user=current_user)

@views.route('/profile', methods=['POST'])
def profile():
    return render_template('myprofile.html')


@views.route('/delete-entry', methods=['POST'])
def delete_entry():
    entry = json.loads(request.data)
    entryId = entry['entryId']
    entry = Entry.query.get(entryId)
    if entry:
        if entry.user_id == current_user.id:
            db.session.delete(entry)
            db.session.commmit()
            
    return jsonify({})


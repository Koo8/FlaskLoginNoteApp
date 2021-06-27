from flask import Blueprint,jsonify,  render_template,flash, request
from flask_login import current_user, login_required
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=["POST", "GET"])
@login_required
def note():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note)<2:
            flash('The note is too short.', category='danger')
        else:
            new_note = Note(note=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template('note.html', user = current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    jasonData = json.loads(request.data)
    noteId = jasonData['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

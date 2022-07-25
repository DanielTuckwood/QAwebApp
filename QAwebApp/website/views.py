from webbrowser import get
from flask import Blueprint, abort, redirect, render_template, flash, request, url_for
from flask_login import login_required, current_user
from . import db
from . models import Note
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

views = Blueprint('views', __name__)


#Home page view
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)    

#Notes page view
@views.route('/notes', methods=['GET','POST'])
@login_required
def note():
    if request.method == 'POST':

        #Getter
        note = request.form.get('note')

        #Validation
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            #Create new note
            new_note = Note(txt=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added.', category='success')

    return render_template("note.html", user=current_user)    

#User Guide Page
@views.route('/userGuide')
@login_required
def userGuide():
    return render_template("userGuide.html", user=current_user)  

#Edit note view
@views.route('/update<int:id>', methods=['GET','POST'])
@login_required      
def update(id): 
    if request.method == 'POST':
        #Getter
        note_to_update = Note.query.get_or_404(id)

        if note.author != current_user:
            abort(403)

        return render_template("update.html", user=current_user)

        
#Delete note view
@views.route('/delete/<int:id>')   
@login_required 
def delete(id):

    #Getter
    note_to_delete = Note.query.get_or_404(id)

    #Attempt to delete
    try:
        db.session.delete(note_to_delete)
        db.session.commit()        
        flash('Note deleted')
        return redirect(url_for('views.note'))

    #Catch error    
    except:
        flash('Error deleting!')
        return redirect(url_for('views.note'))

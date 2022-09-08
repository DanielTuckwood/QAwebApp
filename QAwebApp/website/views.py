from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_required, current_user
from . import db
from . models import Case, Note, User

views = Blueprint('views', __name__)

#Home page view
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':

        #Getters
        sponsorURN = request.form.get('sponsorURN')
        caseType = request.form.get('caseType')
        txt = request.form.get('txt')

       #Validation
        if len(sponsorURN) < 6:
            flash('Sponsor URN is too short!', category='error')
        elif len(caseType) < 10:
            flash('Case Type is too short!', category='error')
        elif len(txt) < 1:
            flash('Case notes too short! If there are no notes, enter - ', category='error')    
        else:
            #Create new case
            new_case = Case(sponsorURN=sponsorURN, case_type=caseType, txt=txt, user_id=current_user.id)
            db.session.add(new_case)
            db.session.commit()
            flash('Case added.', category='success')

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

#Admin view
@views.route('/admin/<int:id>')
@login_required
def checkAdmin(id):

    #Getter
    adminStatus = User.query.get_or_404(id)

    #Check admin status
    if adminStatus.admin == True:
        return render_template("admin.html", user=current_user)
    else:
        flash("Administrator rights required!", category="error")
        return redirect(url_for('views.home'))        
        
#Edit note view
@views.route('/updateCase/<int:id>', methods=['GET','POST'])
@login_required      
def update(id): 

    case_to_update = Case.query.filter_by(id=id).first()
    if request.method == 'POST':
        if case_to_update:
            db.session.delete(case_to_update)
            db.session.commit()
        #Getters
        sponsorURN = request.form.get('sponsorURN')
        caseType = request.form.get('caseType')
        txt = request.form.get('txt')   

        #Create new case
        case_to_update = Case(sponsorURN=sponsorURN, case_type=caseType, txt=txt, user_id=current_user.id)
        db.session.add(case_to_update)
        db.session.commit()
        flash('Case updated.', category='success') 

    return render_template("update.html", user=current_user) 

#Delete note view
@views.route('/deleteNote/<int:id>')   
@login_required 
def deleteNote(id):

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

#Delete case view
@views.route('/deleteCase/<int:id>')   
@login_required 
def deleteCase(id):

    #Getter
    case_to_delete = Case.query.get_or_404(id)

    #Attempt to delete
    try:
        db.session.delete(case_to_delete)
        db.session.commit()        
        flash('Case deleted')
        return redirect(url_for('views.home'))

    #Catch error    
    except:
        flash('Error deleting!')
        return redirect(url_for('views.hpme'))
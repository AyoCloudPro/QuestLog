from .models import db, User, Task, Note
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, logout_user, login_user
from .forms import LoginForm
from datetime import datetime
from .functions import get_greeting, get_random_quotes


import logging

# Logs function
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s]'
)
logger=logging.getLogger(__name__)


# Blueprint function
auth_bp = Blueprint('auth', __name__)


# Login route
# ======================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)
            flash('Welcome back, adventurer. Quests await')
            return redirect(url_for('auth.dashboard'))
        else:
            user = User(username=form.username.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Welcome to QuestLog!')
            return redirect(url_for('auth.dashboard'))
    
    return render_template('login.html', form=form)

# Logout route
# ====================
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye for now. We await your return.')

    return redirect(url_for('auth.login'))


# Authenicated route
# ============================
@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    else:
        return redirect(url_for("auth.login"))
    

# Dashboard route
# ====================
@auth_bp.route('/dashboard')
@login_required
def dashboard():
    greeting = get_greeting()
    quote    = get_random_quotes()
    tasks     = Task.query.filter_by(user_id=current_user.id).all()
    notes    = Note.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard.html', greeting=greeting, quote=quote, tasks=tasks, notes=notes)


# Task add route
# ============
@auth_bp.route('/add-task', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    if title:
        new_task = Task(title=title, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        logger.info(f"User {current_user.username} added a task: {title}") # logs
        flash('A new quest has arrived, comrade.')
        return jsonify({'success': True, 'message': 'Quest added!'}), 200
    else:
        logger.warning(f"User {current_user.username} submitted an empty task") # logs
        return jsonify({'success': False, 'message': 'Title is required'}), 400



# Task in-progress route
# =================
@auth_bp.route('/progress-task/<int:id>', methods=['POST'])
@login_required
def progress_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        task.in_progress = True
        db.session.commit()
        logger.info(f"User {current_user.username} task is in progress: {task.user_id}") # logs
        flash('Taking on a new quest. Excellent')
        return jsonify({'success': True, 'message': 'Quest in progress!'}), 200
    else:
        logger.warning(f"user {current_user.username} is not in progress") # logs
        return jsonify({'success': False, 'message': 'Task failed to be in progress'}), 400


# Task complete route
# ===============
@auth_bp.route('/complete-task/<int:id>', methods=['POST'])
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        task.is_complete = True
        db.session.commit()
        logger.info(f"User {current_user.username} has completed task: {task.user_id}") # logs
        flash('Well done warrior. Every victory is precious.')
        return jsonify({'success': True, 'message': 'Quest completed!'}), 200
    else:
        logger.warning(f"User {current_user.username} task completion failed") # logs
        return jsonify({'success': False, 'message': 'Task completion failed'}), 400


# Task delete route
# ====================
@auth_bp.route('/delete-task/<int:id>', methods=['POST'] )
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        logger.info(f"User {current_user.username} has deleted task: {task.user_id}") # logs
        flash("Did you complete it, or abandon yur duites?")
        return jsonify({'success': True, 'message': 'Quest removed!'}), 200
    else:
        logger.warning(f"User {current_user.username} task delete failed") # logs
        return jsonify({'success': False, 'message': 'Task delete failed'}), 400


# Add notes route
# ==============
@auth_bp.route('/add-note', methods=['POST'])
@login_required
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')
    note = Note(title=title, content=content, user_id=current_user.id)
    db.session.add(note)
    db.session.commit()
    logger.info(f"User {current_user.username} has added a note: {title}") # logs
    flash("A new grimoire. How wonderful!") 
    return jsonify({'success': True, 'message': 'Spell book created!'}), 200


# Edit notes route
# ======================
@auth_bp.route('/edit-note/<int:id>', methods=['POST'])
@login_required
def edit_note(id):
    data = request.get_json()
    note = Note.query.get_or_404(id)
    if note.user_id == current_user.id:
        note.title = data['title']
        note.content = data['content']
        db.session.commit()
        logger.info(f"User {current_user.username} has editted a note: {note.user_id}") # logs
        flash('Fascinating inscriptions.')
        return jsonify({'success': True, 'message': 'Spell book edited!'}), 200
    else:
        logger.info(f"User {current_user.username} note editting failed: {note.user_id}") # logs
        return jsonify({'success': False, 'message': 'Note edit failed'}), 400
    

# Delete notes route
# ==========================
@auth_bp.route('/delete-note/<int:id>', methods=['POST'])
@login_required
def delete_notes(id):
    note = Note.query.get_or_404(id)
    if note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        logger.info(f"User {current_user.username} has deleted a note: {note.user_id}") # logs
        flash("Discarding your gimoire? Old things pass away i suppose.")
        return jsonify({'success': True, 'message': 'Spell book removed'}), 200
    else:
        logger.info(f"User {current_user.username} note deletion failed: {note.user_id}") # logs
        return jsonify({'success': False, 'message': 'Note failed to delete'}), 400
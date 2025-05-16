from . import db
from datetime import datetime, timezone
from flask_login import UserMixin


# User Model
# =============================
class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

    tasks = db.relationship('Task', backref='author', lazy=True)
    notes = db.relationship('Note', backref='author', lazy=True)

# Task Model
# ================
class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(140), nullable=False)
    in_progress = db.Column(db.Boolean, default=False)
    is_complete = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))


# Note Model
# ==================
class Note(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(140), nullable=False)
    content    = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'))


# Delay the import of db
def init_db(app):
    from app import db
    db.init_app(app)

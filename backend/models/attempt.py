from extensions import db
from datetime import datetime

class Attempt(db.Model):
    __tablename__= 'attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"))
    score = db.Column(db.Integer)
    total_questions= db.Column(db.Integer, nullable=False)
    
    created_at= db.Column(db.DateTime, default= datetime.now)
from extensions import db

class Question(db.Model):
    __tablename__='questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"))
    question_text = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.String(1))
    
    options = db.relationship(
        "Option",
        backref="question",
        lazy=True,
        cascade="all, delete-orphan"
    )

class Option(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    option_key = db.Column(db.String(1))
    option_text = db.Column(db.Text)
from extensions import db

class Quiz(db.Model):
    __tablename__= 'quizzes'
    
    id= db.Column(db.Integer, primary_key= True)
    title= db.Column(db.String(80), nullable= False)
    difficulty= db.Column(db.String(120))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    questions = db.relationship(
        "Question",
        backref="quiz",
        lazy=True,
        cascade="all, delete-orphan"
    )


    def __repr__(self):
        return f"<Quiz {self.title}>"
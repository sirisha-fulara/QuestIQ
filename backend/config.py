import os

class Config:
    SECRET_KEY= 'ad7419ac023b98c15824f9014af97e1e'
    SQLALCHEMY_DATABASE_URI= 'postgresql://postgres:siripostgres@localhost:5432/quizdb'
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    JWT_SECRET_KEY= 'aaa1315800ddafa394648ba34a53f199'
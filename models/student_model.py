from datetime import datetime
from models.database import db

class Student(db.Model):
    """学生数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    class_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 建立与成绩表的关系
    scores = db.relationship('Score', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.student_id}: {self.name}>'
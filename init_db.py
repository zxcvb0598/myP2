from app import app
from models.database import init_db
from models.student_model import Student
from models.course_model import Course
from models.score_model import Score
from models.database import db
import datetime

# 初始化数据库
def create_database():
    with app.app_context():
        # 删除现有表（如果存在）
        db.drop_all()
        
        # 创建所有表
        db.create_all()
        
        # 添加示例学生数据
        students = [
            Student(student_id='2023001', name='张三', gender='男', date_of_birth=datetime.date(2005, 1, 15), class_name='计算机科学1班'),
            Student(student_id='2023002', name='李四', gender='女', date_of_birth=datetime.date(2005, 3, 20), class_name='计算机科学1班'),
            Student(student_id='2023003', name='王五', gender='男', date_of_birth=datetime.date(2005, 5, 10), class_name='计算机科学2班'),
            Student(student_id='2023004', name='赵六', gender='女', date_of_birth=datetime.date(2005, 7, 8), class_name='计算机科学2班'),
            Student(student_id='2023005', name='钱七', gender='男', date_of_birth=datetime.date(2005, 9, 12), class_name='计算机科学1班')
        ]
        
        # 添加示例课程数据
        courses = [
            Course(course_code='CS101', course_name='高等数学', credits=4.0, semester='2023-2024学年第一学期'),
            Course(course_code='CS102', course_name='线性代数', credits=3.0, semester='2023-2024学年第一学期'),
            Course(course_code='CS103', course_name='计算机基础', credits=4.0, semester='2023-2024学年第一学期'),
            Course(course_code='CS104', course_name='程序设计', credits=5.0, semester='2023-2024学年第二学期'),
            Course(course_code='CS105', course_name='数据结构', credits=4.0, semester='2023-2024学年第二学期')
        ]
        
        # 添加数据到数据库
        db.session.add_all(students)
        db.session.add_all(courses)
        db.session.commit()
        
        # 添加成绩数据
        scores = [
            # 张三的成绩
            Score(student_id=students[0].id, course_id=courses[0].id, score=85, exam_date=datetime.date(2023, 12, 10)),
            Score(student_id=students[0].id, course_id=courses[1].id, score=78, exam_date=datetime.date(2023, 12, 15)),
            Score(student_id=students[0].id, course_id=courses[2].id, score=92, exam_date=datetime.date(2023, 12, 20)),
            
            # 李四的成绩
            Score(student_id=students[1].id, course_id=courses[0].id, score=90, exam_date=datetime.date(2023, 12, 10)),
            Score(student_id=students[1].id, course_id=courses[1].id, score=85, exam_date=datetime.date(2023, 12, 15)),
            Score(student_id=students[1].id, course_id=courses[2].id, score=88, exam_date=datetime.date(2023, 12, 20)),
            
            # 王五的成绩
            Score(student_id=students[2].id, course_id=courses[0].id, score=65, exam_date=datetime.date(2023, 12, 10)),
            Score(student_id=students[2].id, course_id=courses[1].id, score=72, exam_date=datetime.date(2023, 12, 15)),
            Score(student_id=students[2].id, course_id=courses[2].id, score=68, exam_date=datetime.date(2023, 12, 20)),
            
            # 赵六的成绩
            Score(student_id=students[3].id, course_id=courses[0].id, score=95, exam_date=datetime.date(2023, 12, 10)),
            Score(student_id=students[3].id, course_id=courses[1].id, score=92, exam_date=datetime.date(2023, 12, 15)),
            Score(student_id=students[3].id, course_id=courses[2].id, score=98, exam_date=datetime.date(2023, 12, 20)),
            
            # 钱七的成绩
            Score(student_id=students[4].id, course_id=courses[0].id, score=58, exam_date=datetime.date(2023, 12, 10)),
            Score(student_id=students[4].id, course_id=courses[1].id, score=62, exam_date=datetime.date(2023, 12, 15)),
            Score(student_id=students[4].id, course_id=courses[2].id, score=75, exam_date=datetime.date(2023, 12, 20))
        ]
        
        db.session.add_all(scores)
        db.session.commit()
        
        print("数据库初始化成功，已添加示例数据！")

if __name__ == '__main__':
    create_database()
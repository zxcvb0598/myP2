from flask import render_template, request, redirect, url_for, flash
from app import app
from models.score_model import Score
from models.student_model import Student
from models.course_model import Course
from models.database import db
from datetime import datetime

@app.route('/scores')
def score_list():
    """显示所有成绩列表"""
    # 获取筛选参数
    student_id = request.args.get('student_id', '')
    course_id = request.args.get('course_id', '')
    
    # 构建查询
    query = Score.query.join(Student).join(Course)
    
    if student_id:
        query = query.filter(Score.student_id == student_id)
    if course_id:
        query = query.filter(Score.course_id == course_id)
    
    scores = query.order_by(Student.student_id, Course.course_code).all()
    
    # 获取所有学生和课程用于筛选下拉框
    students = Student.query.order_by(Student.student_id).all()
    courses = Course.query.order_by(Course.course_code).all()
    
    return render_template('score_list.html', 
                          scores=scores, 
                          students=students, 
                          courses=courses, 
                          selected_student_id=student_id, 
                          selected_course_id=course_id)

@app.route('/score/add', methods=['GET', 'POST'])
def add_score():
    """添加成绩记录"""
    # 获取所有学生和课程用于下拉选择
    students = Student.query.order_by(Student.student_id).all()
    courses = Course.query.order_by(Course.course_code).all()
    
    if request.method == 'POST':
        # 获取表单数据
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        score_value = request.form['score']
        exam_date = request.form['exam_date']
        
        # 检查该学生的该课程成绩是否已存在
        existing_score = Score.query.filter_by(student_id=student_id, course_id=course_id).first()
        if existing_score:
            flash('该学生的这门课程成绩已存在，请编辑现有成绩！', 'danger')
            return redirect(url_for('add_score'))
        
        # 验证成绩是否为有效数字
        try:
            score_value = float(score_value)
            if score_value < 0 or score_value > 100:
                raise ValueError
        except ValueError:
            flash('成绩必须是0-100之间的数字！', 'danger')
            return redirect(url_for('add_score'))
        
        # 解析日期
        try:
            exam_date = datetime.strptime(exam_date, '%Y-%m-%d').date() if exam_date else None
        except ValueError:
            flash('日期格式不正确，请使用YYYY-MM-DD格式！', 'danger')
            return redirect(url_for('add_score'))
        
        # 创建新成绩记录
        new_score = Score(
            student_id=student_id,
            course_id=course_id,
            score=score_value,
            exam_date=exam_date
        )
        
        # 添加到数据库
        db.session.add(new_score)
        db.session.commit()
        
        flash('成绩添加成功！', 'success')
        return redirect(url_for('score_list'))
    
    return render_template('add_score.html', students=students, courses=courses)

@app.route('/score/edit/<int:score_id>', methods=['GET', 'POST'])
def edit_score(score_id):
    """编辑成绩信息"""
    score = Score.query.get_or_404(score_id)
    # 获取所有学生和课程用于下拉选择
    students = Student.query.order_by(Student.student_id).all()
    courses = Course.query.order_by(Course.course_code).all()
    
    if request.method == 'POST':
        # 获取表单数据
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        score_value = request.form['score']
        exam_date = request.form['exam_date']
        
        # 检查是否修改了学生或课程，且该组合已存在成绩
        if (student_id != str(score.student_id)) or (course_id != str(score.course_id)):
            existing_score = Score.query.filter_by(student_id=student_id, course_id=course_id).first()
            if existing_score and existing_score.id != score_id:
                flash('该学生的这门课程成绩已存在！', 'danger')
                return redirect(url_for('edit_score', score_id=score_id))
        
        # 验证成绩是否为有效数字
        try:
            score_value = float(score_value)
            if score_value < 0 or score_value > 100:
                raise ValueError
        except ValueError:
            flash('成绩必须是0-100之间的数字！', 'danger')
            return redirect(url_for('edit_score', score_id=score_id))
        
        # 更新成绩信息
        score.student_id = student_id
        score.course_id = course_id
        score.score = score_value
        
        # 解析日期
        try:
            score.exam_date = datetime.strptime(exam_date, '%Y-%m-%d').date() if exam_date else None
        except ValueError:
            flash('日期格式不正确，请使用YYYY-MM-DD格式！', 'danger')
            return redirect(url_for('edit_score', score_id=score_id))
        
        # 保存修改
        db.session.commit()
        
        flash('成绩信息更新成功！', 'success')
        return redirect(url_for('score_list'))
    
    # 格式化日期为YYYY-MM-DD格式用于表单显示
    score.exam_date_str = score.exam_date.strftime('%Y-%m-%d') if score.exam_date else ''
    
    return render_template('edit_score.html', score=score, students=students, courses=courses)

@app.route('/score/delete/<int:score_id>', methods=['GET', 'POST'])
def delete_score(score_id):
    """删除成绩记录"""
    score = Score.query.get_or_404(score_id)
    
    # 删除成绩
    db.session.delete(score)
    db.session.commit()
    
    flash('成绩记录已成功删除！', 'success')
    return redirect(url_for('score_list'))
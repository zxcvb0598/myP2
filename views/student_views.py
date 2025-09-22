from flask import render_template, request, redirect, url_for, flash
from app import app
from models.student_model import Student
from models.database import db
from datetime import datetime

@app.route('/')
def index():
    """首页，重定向到学生列表"""
    return redirect(url_for('student_list'))

@app.route('/students')
def student_list():
    """显示所有学生列表"""
    # 获取搜索参数
    search_query = request.args.get('search', '')
    
    if search_query:
        # 按学号或姓名搜索学生
        students = Student.query.filter(
            (Student.student_id.contains(search_query)) | 
            (Student.name.contains(search_query)) |
            (Student.class_name.contains(search_query))
        ).order_by(Student.student_id).all()
    else:
        # 显示所有学生，按学号排序
        students = Student.query.order_by(Student.student_id).all()
    
    return render_template('student_list.html', students=students, search_query=search_query)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    """添加新学生"""
    if request.method == 'POST':
        # 获取表单数据
        student_id = request.form['student_id']
        name = request.form['name']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        class_name = request.form['class_name']
        
        # 检查学号是否已存在
        existing_student = Student.query.filter_by(student_id=student_id).first()
        if existing_student:
            flash('该学号已存在！', 'danger')
            return redirect(url_for('add_student'))
        
        # 解析日期
        try:
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            flash('日期格式不正确，请使用YYYY-MM-DD格式！', 'danger')
            return redirect(url_for('add_student'))
        
        # 创建新学生
        new_student = Student(
            student_id=student_id,
            name=name,
            gender=gender,
            date_of_birth=date_of_birth,
            class_name=class_name
        )
        
        # 添加到数据库
        db.session.add(new_student)
        db.session.commit()
        
        flash('学生添加成功！', 'success')
        return redirect(url_for('student_list'))
    
    return render_template('add_student.html')

@app.route('/student/<int:student_id>')
def student_detail(student_id):
    """显示学生详情"""
    student = Student.query.get_or_404(student_id)
    return render_template('student_detail.html', student=student)

@app.route('/student/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    """编辑学生信息"""
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        # 获取表单数据
        new_student_id = request.form['student_id']
        name = request.form['name']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        class_name = request.form['class_name']
        
        # 检查学号是否被修改且已存在
        if new_student_id != student.student_id:
            existing_student = Student.query.filter_by(student_id=new_student_id).first()
            if existing_student:
                flash('该学号已存在！', 'danger')
                return redirect(url_for('edit_student', student_id=student_id))
            student.student_id = new_student_id
        
        # 更新其他信息
        student.name = name
        student.gender = gender
        
        # 解析日期
        try:
            student.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            flash('日期格式不正确，请使用YYYY-MM-DD格式！', 'danger')
            return redirect(url_for('edit_student', student_id=student_id))
        
        student.class_name = class_name
        
        # 保存修改
        db.session.commit()
        
        flash('学生信息更新成功！', 'success')
        return redirect(url_for('student_detail', student_id=student_id))
    
    # 格式化日期为YYYY-MM-DD格式用于表单显示
    student.date_of_birth_str = student.date_of_birth.strftime('%Y-%m-%d') if student.date_of_birth else ''
    
    return render_template('edit_student.html', student=student)

@app.route('/student/delete/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    """删除学生"""
    student = Student.query.get_or_404(student_id)
    
    # 删除学生
    db.session.delete(student)
    db.session.commit()
    
    flash('学生已成功删除！', 'success')
    return redirect(url_for('student_list'))
from flask import render_template, request, redirect, url_for, flash
from app import app
from models.course_model import Course
from models.database import db
from flask import request, flash, redirect, url_for

@app.route('/courses')
def course_list():
    """显示所有课程列表"""
    # 获取搜索参数
    search_query = request.args.get('search', '')
    
    if search_query:
        # 按课程代码或名称搜索课程
        courses = Course.query.filter(
            (Course.course_code.contains(search_query)) | 
            (Course.course_name.contains(search_query)) |
            (Course.semester.contains(search_query))
        ).order_by(Course.course_code).all()
    else:
        # 显示所有课程，按课程代码排序
        courses = Course.query.order_by(Course.course_code).all()
    
    return render_template('course_list.html', courses=courses, search_query=search_query)

@app.route('/course/add', methods=['GET', 'POST'])
def add_course():
    """添加新课程"""
    if request.method == 'POST':
        # 获取表单数据
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        credits = request.form['credits']
        semester = request.form['semester']
        
        # 检查课程代码是否已存在
        existing_course = Course.query.filter_by(course_code=course_code).first()
        if existing_course:
            flash('该课程代码已存在！', 'danger')
            return redirect(url_for('add_course'))
        
        # 验证学分是否为有效数字
        try:
            credits = float(credits)
            if credits <= 0:
                raise ValueError
        except ValueError:
            flash('学分必须是大于0的数字！', 'danger')
            return redirect(url_for('add_course'))
        
        # 创建新课程
        new_course = Course(
            course_code=course_code,
            course_name=course_name,
            credits=credits,
            semester=semester
        )
        
        # 添加到数据库
        db.session.add(new_course)
        db.session.commit()
        
        flash('课程添加成功！', 'success')
        return redirect(url_for('course_list'))
    
    return render_template('add_course.html')

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    """显示课程详情"""
    course = Course.query.get_or_404(course_id)
    # 获取选修该课程的学生及成绩
    scores = course.scores
    
    return render_template('course_detail.html', course=course, scores=scores)

@app.route('/course/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    """编辑课程信息"""
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        # 获取表单数据
        new_course_code = request.form['course_code']
        course_name = request.form['course_name']
        credits = request.form['credits']
        semester = request.form['semester']
        
        # 检查课程代码是否被修改且已存在
        if new_course_code != course.course_code:
            existing_course = Course.query.filter_by(course_code=new_course_code).first()
            if existing_course:
                flash('该课程代码已存在！', 'danger')
                return redirect(url_for('edit_course', course_id=course_id))
            course.course_code = new_course_code
        
        # 更新其他信息
        course.course_name = course_name
        
        # 验证学分是否为有效数字
        try:
            course.credits = float(credits)
            if course.credits <= 0:
                raise ValueError
        except ValueError:
            flash('学分必须是大于0的数字！', 'danger')
            return redirect(url_for('edit_course', course_id=course_id))
        
        course.semester = semester
        
        # 保存修改
        db.session.commit()
        
        flash('课程信息更新成功！', 'success')
        return redirect(url_for('course_detail', course_id=course_id))
    
    return render_template('edit_course.html', course=course)

@app.route('/course/delete/<int:course_id>', methods=['GET', 'POST'])
def delete_course(course_id):
    """删除课程"""
    course = Course.query.get_or_404(course_id)
    
    # 删除课程
    db.session.delete(course)
    db.session.commit()
    
    flash('课程已成功删除！', 'success')
    return redirect(url_for('course_list'))
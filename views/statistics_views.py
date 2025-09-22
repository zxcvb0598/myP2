from flask import render_template, request
from app import app
from models.student_model import Student
from models.course_model import Course
from models.score_model import Score
from models.database import db

@app.route('/statistics')
def statistics_dashboard():
    """统计分析首页"""
    # 获取统计数据
    student_count = Student.query.count()
    course_count = Course.query.count()
    score_count = Score.query.count()
    
    # 计算平均成绩
    all_scores = Score.query.all()
    if all_scores:
        average_score = sum([s.score for s in all_scores]) / len(all_scores)
    else:
        average_score = 0
    
    # 计算成绩分布
    score_distribution = {
        '0-59': 0,
        '60-69': 0,
        '70-79': 0,
        '80-89': 0,
        '90-100': 0
    }
    
    for score in all_scores:
        if score.score < 60:
            score_distribution['0-59'] += 1
        elif score.score < 70:
            score_distribution['60-69'] += 1
        elif score.score < 80:
            score_distribution['70-79'] += 1
        elif score.score < 90:
            score_distribution['80-89'] += 1
        else:
            score_distribution['90-100'] += 1
    
    # 获取平均分最高的5门课程
    courses = Course.query.all()
    top_courses = []
    for course in courses:
        if course.scores:
            course_avg = sum([s.score for s in course.scores]) / len(course.scores)
            top_courses.append({
                'course_name': course.course_name,
                'average_score': course_avg
            })
    
    # 按平均分排序，取前5个
    top_courses.sort(key=lambda x: x['average_score'], reverse=True)
    top_courses = top_courses[:5]
    
    return render_template('statistics_dashboard.html',
                          student_count=student_count,
                          course_count=course_count,
                          score_count=score_count,
                          average_score=average_score,
                          score_distribution=score_distribution,
                          top_courses=top_courses)

@app.route('/statistics/course')
def statistics_by_course():
    """按课程统计成绩"""
    # 获取所有课程
    courses = Course.query.order_by(Course.course_code).all()
    
    # 统计每个课程的成绩信息
    course_stats = []
    for course in courses:
        scores = course.scores
        if scores:
            # 计算统计数据
            score_values = [s.score for s in scores]
            avg_score = sum(score_values) / len(score_values)
            max_score = max(score_values)
            min_score = min(score_values)
            student_count = len(score_values)
            fail_count = len([s for s in scores if s.score < 60])
            fail_rate = (fail_count / student_count) * 100 if student_count > 0 else 0
            
            course_stats.append({
                'course_name': course.course_name,
                'course_code': course.course_code,
                'credits': course.credits,
                'student_count': student_count,
                'average_score': avg_score,
                'max_score': max_score,
                'min_score': min_score,
                'fail_rate': fail_rate
            })
    
    return render_template('statistics_by_course.html', course_stats=course_stats)

@app.route('/statistics/student')
def statistics_by_student():
    """按学生统计成绩"""
    # 获取所有学生
    students = Student.query.order_by(Student.student_id).all()
    
    # 统计每个学生的成绩信息
    student_stats = []
    for student in students:
        scores = student.scores
        if scores:
            # 计算统计数据
            score_values = [s.score for s in scores]
            avg_score = sum(score_values) / len(score_values)
            total_score = sum(score_values)
            course_count = len(score_values)
            max_score = max(score_values)
            min_score = min(score_values)
            fail_courses = len([s for s in scores if s.score < 60])
            
            student_stats.append({
                'name': student.name,
                'student_id': student.student_id,
                'class_name': student.class_name,
                'course_count': course_count,
                'average_score': avg_score,
                'total_score': total_score,
                'max_score': max_score,
                'min_score': min_score,
                'fail_courses': fail_courses
            })
    
    return render_template('statistics_by_student.html', student_stats=student_stats)

@app.route('/statistics/detail')
def detailed_statistics():
    """详细统计分析页面"""
    # 获取所有学生和课程的数量
    all_scores = Score.query.all()
    total_scores = len(all_scores)
    
    # 计算各分数段的整体分布
    score_distribution = {
        '0-59': 0,
        '60-69': 0,
        '70-79': 0,
        '80-89': 0,
        '90-100': 0
    }
    
    for score in all_scores:
        if score.score < 60:
            score_distribution['0-59'] += 1
        elif score.score < 70:
            score_distribution['60-69'] += 1
        elif score.score < 80:
            score_distribution['70-79'] += 1
        elif score.score < 90:
            score_distribution['80-89'] += 1
        else:
            score_distribution['90-100'] += 1
    
    # 统计各班级平均成绩
    students = Student.query.all()
    class_scores = {}
    class_students = {}
    
    for student in students:
        if student.class_name not in class_scores:
            class_scores[student.class_name] = []
            class_students[student.class_name] = 0
        
        class_students[student.class_name] += 1
        
        for score in student.scores:
            class_scores[student.class_name].append(score.score)
    
    class_averages = {}
    for class_name, scores in class_scores.items():
        if scores:
            class_averages[class_name] = sum(scores) / len(scores)
    
    # 统计各学期课程数量
    courses = Course.query.all()
    semester_courses = {}
    
    for course in courses:
        semester = course.semester if course.semester else '未设置'
        if semester not in semester_courses:
            semester_courses[semester] = 0
        semester_courses[semester] += 1
    
    # 找出成绩优秀的学生（平均分≥90）
    top_students = []
    for student in students:
        if student.scores:
            avg_score = sum([s.score for s in student.scores]) / len(student.scores)
            if avg_score >= 90:
                top_students.append({
                    'name': student.name,
                    'student_id': student.student_id,
                    'average_score': avg_score
                })
    
    # 找出难度较大的课程（平均分<70）
    challenging_courses = []
    for course in courses:
        if course.scores:
            avg_score = sum([s.score for s in course.scores]) / len(course.scores)
            if avg_score < 70:
                fail_count = len([s for s in course.scores if s.score < 60])
                fail_rate = (fail_count / len(course.scores)) * 100 if len(course.scores) > 0 else 0
                challenging_courses.append({
                    'course_name': course.course_name,
                    'course_code': course.course_code,
                    'average_score': avg_score,
                    'fail_rate': fail_rate
                })
    
    return render_template('detailed_statistics.html',
                          score_distribution=score_distribution,
                          total_scores=total_scores,
                          class_averages=class_averages,
                          class_students=class_students,
                          semester_courses=semester_courses,
                          top_students=top_students,
                          challenging_courses=challenging_courses)
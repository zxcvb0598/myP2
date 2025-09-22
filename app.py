from flask import Flask, render_template, request, redirect, url_for, flash
from models.database import init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
init_db(app)

# 导入视图
from views.student_views import *
from views.course_views import *
from views.score_views import *
from views.statistics_views import *

if __name__ == '__main__':
    app.run(debug=True)
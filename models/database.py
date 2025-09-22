from flask_sqlalchemy import SQLAlchemy

# 创建SQLAlchemy实例
db = SQLAlchemy()

def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    # 在应用上下文中创建数据库表
    with app.app_context():
        db.create_all()
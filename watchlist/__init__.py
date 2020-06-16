#!/usr/bin/python3
# @FileName    :__init__.py
# @Time        :2020/6/16 下午9:04
# @Author      :ABC
# @Description : 包构造文件，创建程序实例
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),
                                                              os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 初始化扩展，传入程序实例 app,在扩展类实例化前加载配置
db = SQLAlchemy(app)
# 实例化扩展类
login_manager = LoginManager(app)
# 把 login_manager.login_view 的值设为我们程序的登录视图端点（函数名）
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    # 在这里导入User是为了避免循环依赖(A导入B，B导入A)
    from watchlist.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


@app.context_processor
def inject_user():
    # 在这里导入User是为了避免循环依赖(A导入B，B导入A)
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


'''
在构造文件中，为了让视图函数、错误处理函数和命令函数注册到程序实例上，我们需要在这里导入这几个模块。
但是因为这几个模块同时也要导入构造文件中的程序实例，为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾。
'''
from watchlist import views, errors, commands

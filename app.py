# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time      : 2020/6/15 下午3:11
# @Author    : ABC
# @FileName  : app.py
import os
import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类

app = Flask(__name__)

'''
写入了一个 SQLALCHEMY_DATABASE_URI 变量(sqlite:////数据库文件的绝对地址)来告诉 SQLAlchemy 数据库连接地址
数据库文件一般放到项目根目录即可，app.root_path 返回程序实例所在模块的路径（目前来说，即项目根目录），我们使用它来构建文件路径。
数据库文件的名称和后缀你可以自由定义，一般会使用 .db、.sqlite 和 .sqlite3 作为后缀。
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
# print(app.config.get('SQLALCHEMY_DATABASE_URI'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 初始化扩展，传入程序实例 app,在扩展类实例化前加载配置
db = SQLAlchemy(app)


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # id: Integer类型，主键
    name = db.Column(db.String(20))  # 名字: Sting类型,长度最长为20


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # id: Integer类型，主键
    title = db.Column(db.String(60))  # 电影标题,Sting类型,长度最长为60
    year = db.Column(db.String(4))  # 电影年份,Sting类型,长度最长为4


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'anonymous'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


if __name__ == '__main__':
    app.run(debug=True)

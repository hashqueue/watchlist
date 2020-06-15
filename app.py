# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time      : 2020/6/15 下午3:11
# @Author    : ABC
# @FileName  : app.py
import os
import click

from flask import Flask, render_template, request, flash, redirect, url_for
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


@app.context_processor
def inject_user():  # 函数名可以随意修改
    '''
    模板上下文处理函数
    :return: dict: 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用。
    '''
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}


# 视图函数
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是POST请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')  # 传入表单对应输入字段的 name 值
        if not title or not year or len(title) > 60 or len(year) > 4:
            # 其中 flash() 函数用来在视图函数里向模板传递提示消息，get_flashed_messages() 函数则用来在模板中获取提示消息。
            flash('请输入表单内容或检查movie标题长度是否<=60或检查movie年份长度是否<=4!')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('添加成功!')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    # 使用了 get_or_404() 方法，它会返回对应主键的记录，如果没有找到，则返回 404 错误响应。
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        new_title = request.form['title']
        new_year = request.form['year']

        if not new_title or not new_year or len(new_year) > 4 or len(new_title) > 60:
            flash('请输入表单内容或检查movie标题长度是否<=60或检查movie年份长度是否<=4!')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = new_title  # 更新标题
        movie.year = new_year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('保存成功!')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('删除成功!')
    return redirect(url_for('index'))  # 重定向回主页


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码


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

# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time      : 2020/6/15 上午11:04
# @Author    : ABC
# @FileName  : main.py
from flask import Flask, render_template

app = Flask(__name__)

# 构造虚拟数据
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


# 视图函数
@app.route('/')
def index():
    '''
    在传入render_template() 函数的关键字参数中，
    左边的 movies 是模板中使用的变量名称，右边的 movies 则是该变量指向的实际对象。
    这里传入模板的 name 是字符串，movies 是列表，但能够在模板里使用的不只这两种 Python 数据结构，你也可以传入元组、字典、函数等。
    :return: index.html文件
    '''
    return render_template('index.html', name=name, movies=movies)


if __name__ == '__main__':
    app.run(debug=True)

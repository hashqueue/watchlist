#!/usr/bin/python3
# @FileName    :errors.py
# @Time        :2020/6/16 下午9:05
# @Author      :ABC
# @Description : 错误处理函数
from flask import render_template

from watchlist import app


@app.errorhandler(400)  # 传入要处理的错误代码
def bad_request(e):  # 接受异常对象作为参数
    return render_template('errors/400.html'), 400  # 返回模板和状态码


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

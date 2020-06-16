#!/usr/bin/python3
# @FileName    :wsgi.py
# @Time        :2020/6/16 下午11:52
# @Author      :ABC
# @Description :加载环境变量，并导入程序实例以供部署时使用
import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from watchlist import app

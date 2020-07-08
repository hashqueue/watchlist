## flask学习demo
### 一个观影清单小程序
[点我查看本项目demo对应的教程](https://read.helloflask.com/)
### 部署相关

采用flask+uwsgi部署的项目

* 部署命令：`nohup uwsgi --socket 0.0.0.0:5000 --protocol=http -p 3 -w watchlist:app >> watchlist.log 2>&1 &`
* 参考帖子
    * [Flask学习之旅--Flask项目部署](https://www.cnblogs.com/TM0831/p/11643128.html)
    * [centos下python3.6安装uwsgi失败的解决方法](https://www.cnblogs.com/ingen42/p/10791957.html)


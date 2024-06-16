# mini_blog

## 这是一个前后端结合的网站, 采用Flask框架开发 <br> 如果想在本地运行该网站, 需要:

1. 在requirement.txt查看是否安装了必须的第三方库
2. 在apps/cfg.py里修改为你的信息
3. 打开db.sql文件创建数据库
4. 迁移同步你的MySQL数据库
```
   flask db init 初始化迁移文件
   flask db migrate 生成迁移文件
   flask db upgrade 迁移同步到你的MySQL数据库中
```

5. 注意在启动app.py时, 需要先启动redis服务
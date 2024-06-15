show databases;

-- 创建数据库！！！
create database if not exists mini_blog charset=utf8mb4;


use mini_blog;

truncate table tb_article;

delete
from tb_article
where user_id=1;

show tables;
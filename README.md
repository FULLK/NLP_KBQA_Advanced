

# 参考
[https://github.com/Xiaoheizi2023/NLP_KBQA](https://github.com/Xiaoheizi2023/NLP_KBQA)

# 可视化逻辑
- 提取出实体后去neo4j搜寻实体相关的图谱，然后返回数据再进行可视化
- 可视化工具 cytoscape.js
- 提取实体逻辑：分词后比对关键词


# 运行
数据库：Mysql(保存聊天和用户和帖子信息)    neo4j(保存图谱信息)
后端：flask  blueprint
前端：三件套


```bash
pip install -r requirements.txt
 
启动neo4j 和mysql，记得改用户名和密码

建立图谱和建立关键词表

flask-sqlalchemy通过命令行初始化生成mysql数据库

运行Flask服务器
```

# 演示

[video(video-BWGhm7aC-1734320640826)(type-csdn)(url-https://live.csdn.net/v/embed/439037)(image-https://i-blog.csdnimg.cn/img_convert/e997847ec3415f3cad0c6b611ef2c424.jpeg)(title-演示视频)]




# exts.py：这个文件存在的意义就是为了解决循环引用的问题

# flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from chatbot_graph import ChatBotGraph

db = SQLAlchemy()
mail = Mail()
# 初始化模型
handler = ChatBotGraph()

SECRET_KEY = "asdfasdfjasdfjasd;lf"

# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT= '3306'
DATABASE = 'flask'
USERNAME = 'root'
PASSWORD = '19948703640'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
JSON_AS_ASCII=False

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "zhmbreeze@foxmail.com"
MAIL_PASSWORD = "sbrsvuvpibvfchjg"
MAIL_DEFAULT_SENDER = "zhmbreeze@foxmail.com"
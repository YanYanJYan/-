import os


class Config:
    # MySQL
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'monitor_user'
    MYSQL_PASSWORD = '123'   # 替换成你自己的真实密码
    MYSQL_DB = 'monitor_db'

    # Redis
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0

    # Celery broker/backend
    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/2'

    # 告警邮件（可选，暂不配置）
    MAIL_SERVER = ''
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    ALERT_RECIPIENT = ''

    # 采集间隔（秒）
    COLLECT_INTERVAL = 60
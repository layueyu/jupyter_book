# django存储session

## 安装包
- `pip3 install django-redis-sessions`

## 修改settings文件，添加如下信息
SESSION_ENGINE='redis_session.session'
SESSION_REDIS_HOST='localhost'
SESSION_REDIS_PORT=6379
SESSION_REDIS_DB=2
SESSION_REDIS_PASSWORD=''
SESSION_REDIS_PREFIX='session'
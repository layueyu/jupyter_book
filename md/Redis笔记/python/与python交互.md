# 与python交互

## 安装包
- pip3 install redis

## 调用模块
- 引入模块
    - `from redis import *`
- 使用 StrictRedis 连接Redis
    - `sr = StrictRedis(host='localhost', port=6379, db=0)`
    - 简写：`sr = StrictRedis()`

## 参考文档
- [http://python.jobbole.com/87305/](http://python.jobbole.com/87305/)

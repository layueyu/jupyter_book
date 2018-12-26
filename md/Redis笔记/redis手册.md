# Redis

## 简介
- 开源，使用ANSI C语言编写、支持网络、基于内存亦可持久化的日志型、Key-Value的数据库

## 特性
- 1. 支持数据持久化，可以将内存中的数据保存到磁盘中
- 2. 不仅仅支持简单的key-value类型数据，同时提供list、set、zset、hash等数据结构的存储
- 3. 支持数据备份，即 master-slave模式数据备份 

## 优势
- 1. 性能极高，read：110000次/s write：81000次/s
- 2. 丰富数据类型，支持二进制的Strings,Lists,Hashes,Sets及Oedered Sets 数据类型
- 3. 所有操作都是原子性的，同时支持对几个操作全合并后的原子性执行
- 4. 丰富的特性-Redis支持publish/subscribe，通知，key过期等等

## 应用场景
- 1. 用来做缓存--redis的所有数数据是放在内存中(内存数据库)
- 2. 某些特定场景下代替传统数据库--比如社交类应用
- 3. 在大型系统中，巧妙的实现一些特定功能：session共享、购物车

## 安装redis
- 1. Ubuntu
    - ` sudo apt-get install redis-server `
- 说明：
    - redis-server Redis服务端
    - redis-cli  Redis命令行客户端
    - redis-benchmark redis性能测试工具
    - redis-check-aof AOF文件修复工具
    - redis-check-rdb RDB文件检索工具

- 2. Centos
    - 下载安装包

        - `wget http://download.redis.io/releases/redis-5.0.0.tar.gz`
    - 解包并安装
        - `tar xvzf redis-5.0.0.tar.gz`
        - `cd redis-5.0.0`
        - `make`
        - `make install`
    - 通过初始化脚本启动redis
        - 1. 配置初始化脚本（./utils/redis_init_script)
            - 将初始化脚本复制到/etc/init.d 目录中，文件名为 redis_端口号，其中端口号表示要让Redis监听的端口号，客户端通过该端口连接Redis。然后修改脚本第6行的REDISPORT变量的值为同样的端口号
        - 2. 建立以下需要的文件夹
            - /etc/redis 存放Redis的配置文件
            - /var/redis/端口号 存放Redis的持久化文件
        
        - 3. 修改配置文件
            首先将配置文件模板（redis-5.0.0/redis.conf）复制到/etc/redis 目录中，以端口号命名（如“6379.conf”），然后按照下表对其中的部分参数进行编辑

            参数 | 值 | 说明
            --- | --- | --- 
            daemonize | yes | 使Redis以守护进程模式运行
            pidfile | /var/run/redis_端口号.pid | 设置Redis的PID文件位置
            port | 端口号 | 设置Redis监听的端口号
            dir | /var/redis/端口号 | 设置持久化文件存放位置

        - 4. 启动/关闭服务
            - `service redis_6379 start` 
            - `service redis_6379 stop` 
        
        - 5. 设置开机启动
            - `chkconfig redis_6379 on`

## 配置Redis
- 配置文件路径： /etc/redis/redis.conf
- 核心配置项：
    - 绑定IP：
        - bind 127.0.0.1 ::1 
    - 端口，默认6379
        - port 6379
    - 是否以守护进程运行
        - 若以守护进程运行，不会在命令行阻塞，类似于服务
        - 若以非守护进程运行，则会阻塞当前终端
        - 设置为yes 表示守护进程，设置为no表示非守护进程
        - 推荐设置为 yes
        - daemonize yes
    - 数据文件
        - dbfilename dump.rdb
    - 数据文件路径
        - dir /var/lib/redis
    - 日志文件
        - logfile /var/log/redis/redis-server.log
    - 数据库，默认16个
        - databases 16
    - 主从复制，类似于双机备份
        - slaveof 

## 服务端命令
- 获取帮助
    - `redis-server --help `
- 启动redis服务
    - ` sudo systemctl start redis`
    - ` sudo service redis start`
    - ` sudo redis-server /etc/redis/redis.conf` 指定加载的配置文件
- 停止redis服务
    - ` sudo systemctl stop redis`
    - ` sudo service redis stop`
    - ` sudo kill -9 pid` 杀死redis服务进程
- 重新启动redis服务
    - ` sudo systemctl restart redis`
    - ` sudo service redis restart`

## 客户端命令
- 查看帮助
    - ` redis-cli --help`
- 连接redis
    - ` redis-cli`
- 运行测试命令
    - ` ping `
- 切换数据库
    - 数据库没有名称，你默认16个，通过0-15来标识，连接redis默认选择第一个数据库
    - select n

## 数据操作

### 数据机构
- key-value数据结构，每条数据都是一个键值对
- 键的类型是字符串
- 键不能重复
- 值的类型
    - 字符串型string
    - 哈希hash
    - 列表list
    - 集合set
    - 有序集合zset

### 数据操作行为
- 保存
- 修改
- 获取
- 删除

### String 类型
- 最为基础的数据存储类型
- 是二进制安全的，意味着可以接受任何格式的的数据
- 最多容纳数据长度512M
- 操作：
    - 保存
        - 设置键值
            - ` set key value`
        - 设置键值及过期时间，以秒为单位
            - ` setex key seconds value`
        - 设置多个键值
            - ` mset key1 value1 key2 value2 ... `
        - 追加值
            - ` append key value`
    - 获取
        - 根据键值获取
            - ` get key `
        - 根据多个键获取多个值
            - ` mget key1 key2 ...`
    - 删除
        - 参见键命令

### 键命令
- 查看所有的键
    - ` keys `
- 查看名称中包含a的键
    - ` keys a*`
- 判断键是否存在，如果存在返回1，不存在返回0
    - ` exists key`
- 查看键对应value对应的类型
    - ` type key`
- 删除键及对应的值
    - ` del key1 key2 ...`
- 设置过期时间，以秒为单位
    - 不指定过期时间则一直存在，直到使用DEL删除
    - ` expire key seconds `
- 查看有效时间，以秒为单位
    - ttl key

### hash类型
- 用于存取对象，对象的机构为属性、值
- 值的类型为string
- 操作：
    - 增加
        - 增加、修改
            - ` hset key field value `
        - 设置多个属性
            - ` hset key field1 value1 field2 value2 ...`
    - 获取
        - 获取指定键的说有属性
            - ` hkeys key`
        - 获取一个属性的值
            - ` hget key field`
        - 获取多个属性的值
            - ` hmget key field1 field2 ...`
        - 获取所有属性的值
            - ` hvals key `
    - 删除
        - 删除整个hash键与值，使用del命令
        - 删除属性，属性对应的值会被一起删除
            - ` hdel key field1 field2 ...`

### list类型
- 元素类型String
- 按插入顺序排序
- 操作：
    - 增加
        - 在左侧插入数据
            - ` lpush key value1 value2 ... `
        - 在右侧插入数据
            - ` rpush key value1 value2 ... `
        - 在指定的元素前或后插入数据
            - ` linsert key before或after 现有元素 新元素`
    - 获取
        - 获取列表指定范围的元素
            - satrt，stop为元素的下标索引
            - 索引从左侧开始，第一个元素为0
            - 索引可以是负数，表示从尾部开始计数，如-1表示最后一个元素
            - lrange key start stop
    - 设置指定索引位置的元素的值
        - lset key index value 
    - 删除
        - 删除指定的元素
            - 将列表中前count次出现的值为value的元素移除
            - count > 0 从头到尾移除
            - count < 0 从尾到头移除
            - count = 0 移除所有
            - lrem key count value  

### set类型
- 无序集合
- 元素string类型
- 元素具有唯一性，不重复
- 没有修改操作
- 操作：
    - 增加
        - `sadd key member1 member2 ...`
    - 获取
        - `smembers key`
    - 删除
        - 删除指定元素
            - `srem key member1 member2 ...`

### zset类型
- 有序集合
- 元素string类型
- 元素具有唯一性，不重复
- 每个元素都会关联一个double类型的score，表示权重，通过权重将元素由小到大排序
- 没有修改操作
- 操作：
    - 添加
        - `zadd key score1 member1 score2 member2 ...`
    - 获取
        - 获取指定范围内的元素
            - satrt，stop为元素的下标索引
            - 索引从左侧开始，第一个元素为0
            - 索引可以是负数，表示从尾部开始计数，如-1表示最后一个元素
            - `zrange key start stop`
        - 获取score值在min和max之间的成员
            - `zrangebyscore key min max`
        - 获取成员member的score值
            - `zscore key member`
    - 删除
        - 删除指定的元素
            - `zrem key member1 member2`
        - 删除权重在指定范围的元素
            - `zremrangebyscore key min max`
### redis命令参考 
- [http://doc.redisfans.com/](http://doc.redisfans.com/)
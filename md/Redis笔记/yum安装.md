# yum 安装 redis

#### 1. 安装fedora的epel仓库

```shell
yum install epel-release
```

#### 2. 安装redis数据库

```shell
yum install redis
```

#### 3. 启动服务

```shell
# 启动服务
systemctl start redis

# 停止服务
systemctl stop redis
```

#### 4. 设置开机启动

```shell
systemctl enable redis
```








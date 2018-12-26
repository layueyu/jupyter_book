# centos 安装docker

## yum安装

```bash
yum install docker -y
```

## 启动服务

```bash
# 启动服务
systemctl start docker

# 设置开机启动
systemctl enable docker

# 重启docker
systemctl restart docker

```



## docker 安装

#### 下载镜像

```bash
docker pull redis
```

#### 启动容器




# docker 安装 FTP

### 下载镜像

```bash
docker pull stilliard/pure-ftpd
```

##运行

```bash
# 创建volume
docker volume create --name ftpserver-db-volume

# 启动服务
docker run -d --name ftp_server --restart=always -p 21:21 -p 30000-30209:30000-30209 -e "PUBLICHOST=localhost" -e FTP_USER_NAME=admin -e FTP_USER_PASS=admin -e FTP_USER_HOME=/home/ftpusers/admin --privileged=true -v /home/ftp:/home/ftpusers/admin -v ftpserver-db-volume:/etc/pure-ftpd/passwd stilliard/pure-ftpd bash /run.sh -c 30 -C 10 -l puredb:/etc/pure-ftpd/pureftpd.pdb -E -j -R -P localhost -p 30000:30209
```

- 说明：
  - 满足用户同时登陆，开放端口计算；计算方式为“(最大端口号-最小端口号) / 2
  - 将本机的/home/ftp目录映射到/home/ftpusers/admin



## 其他配置

#### 登陆pure-ftp容器

```bash
docker exec -it ftpd_server /bin/bash
```

创建用户

```bash
pure-pw useradd www -u ftpuser -d /home/ftpusers/www
```

保存

```bash
pure-pw mkdb
```

运行

```
/usr/sbin/pure-ftpd -c 100 -C 100 -l puredb:/etc/pure-ftpd/pureftpd.pdb -E -j -R -P $PUBLICHOST -p 30000:30209 &
```

### 参考文档

- [Docker使用pure-ftp的方法及配置](https://www.bbsmax.com/A/gVdnm1XE5W/)
- [Docker Pure-ftpd Server](https://hub.docker.com/r/stilliard/pure-ftpd/)
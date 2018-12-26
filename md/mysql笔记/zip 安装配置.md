# 1. 下载 zip版本
- [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)

# 2. 解压
- 解压，并进入目录

# 3. 配置环境变量
- C:\Program Files\mysql-5.6.39-winx64\bin

# 4. 初始化
- 删除目录下的data目录
- mysqld --initialize-insecure --user=mysql

# 5. 安装MySQL服务
- mysqld install

# 6. 启动服务
- net start mysql

# 7. 修改root密码
- ALTER user 'root'@'localhost'IDENTIFIED BY '123456';
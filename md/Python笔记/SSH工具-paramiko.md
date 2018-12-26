SSH 工具 paramiko 使用

## SSH 工具类

```java
# -*- coding:utf-8 -*-
import os
import sys
from stat import S_ISDIR

import paramiko


class SSHUtil(object):
    '''
    SSH 工具类
    '''
    def __init__(self, server, user='root', password=None, port=22):
        '''
        初始化
        :param server: 服务器IP
        :param user: 用户名
        :param password: 用户密码
        :param port: 端口号
        '''
        self.user = user
        self.password = password
        self.server = server
        self.port = port
        self.__ssh = None

    def connect(self):

        '''
        与服务器建立连接
        :return:
        '''

        try:
            self.__ssh = paramiko.SSHClient()
            self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.__ssh.connect(hostname=self.server, port=self.port,
                               username=self.user, password=self.password)
            print("连接到主机")
        except Exception as e:
            print("未能连接到主机:{}", e.__str__())

    def cmd(self, cmd):
        '''
        执行命令
        :param cmd:
        :return:
        '''
        stdin, stdout, stderr = self.__ssh.exec_command(cmd)
        result = stdout.read(), stderr.read()
        self.__cmd_result_callback(result, cmd)

    def __cmd_result_callback(self, result, cmd):
        '''
        处理执行命令的后的信息
        :param result:
        :return:
        '''
        print('========== 执行命令：{} ==========='.format(cmd))
        for msg in result:
            print(msg.decode('utf8'))
        print('========== 执行命令：{}, 结束 ==========='.format(cmd))

    def put_file(self, local_file, remote_file):
        '''
        上传文件

        :param local_file:
        :param remote_file:
        :return:
        '''
        try:
            sftp = self.__ssh.open_sftp()
            sftp.put(local_file, remote_file)
            sftp.close()
            print('上传文件成功')
        except Exception as e:
            print('上传文件失败：', e.__str__())

    def get_file(self, remote_file, local_file):
        '''
        下载文件
        :param remote_file:
        :param local_file:
        :return:
        '''
        try:
            sftp = self.__ssh.open_sftp()
            sftp.get(remote_file, local_file)
            sftp.close()
            print("下载文件成功")
        except Exception as e:
            print("下载文件失败:", e.__str__())

    def __get_all_files_in_remote_dir(self, sftp, remote_dir, dirname=None):
        '''
        获取远程目录的所有文集
        :param sftp:
        :param remote_dir:
        :return:
        '''
        # 保存所有文件的列表
        all_files = list()

        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        files = sftp.listdir_attr(remote_dir)
        for x in files:
            filename = remote_dir + '/' + x.filename
            if S_ISDIR(x.st_mode):
                if dirname is not None:
                    all_files.append((dirname+'/'+x.filename, True))
                    all_files.extend(self.__get_all_files_in_remote_dir(sftp, filename, dirname+'/'+x.filename))
                else:
                    all_files.append((x.filename, True))
                    all_files.extend(self.__get_all_files_in_remote_dir(sftp, filename, x.filename))
            else:
                if dirname is not None:
                    all_files.append((dirname+'/'+x.filename, False))
                else:
                    all_files.append((x.filename, False))
        return all_files

    def get_dir(self, remote_dir, local_dir):
        '''
        下载目录
        :param remote_dir:
        :param local_dir:
        :return:
        '''
        try:
            sftp = self.__ssh.open_sftp()
            all_files = self.__get_all_files_in_remote_dir(sftp, remote_dir)
            print('all_files:', all_files)
            for x, dir_flag in all_files:
                filename = x
                local_filename = os.path.join(local_dir, filename)
                if dir_flag:
                    os.mkdir(local_filename)
                else:
                    remote_file = remote_dir+'/'+x
                    print('Get文件{}传输中...'.format(remote_file))
                    sftp.get(remote_file, local_filename)
            sftp.close()
        except Exception as e:
            print("下载目录失败：", e.__str__())


    def __get_all_files_in_local_dir(self, local_dir, dirname=None):
        '''
        获取本地目录的所有文集
        :param local_dir:
        :return:
        '''
        # 保存所有文件的列表
        all_files = list()

        # if local_dir[-1] == '/':
        #     local_dir = local_dir[0:-1]

        # 获取本地目录的属性值
        files = os.listdir(local_dir)
        for x in files:
            filename = os.path.join(local_dir, x)
            # 如果是目录, 则递归处理该目录
            if os.path.isdir(filename):

                if dirname is not None:
                    all_files.append(dirname + '/' + x)
                    all_files.extend(self.__get_all_files_in_local_dir(filename, dirname +'/'+ x))
                else:
                    all_files.append(x)
                    all_files.extend(self.__get_all_files_in_local_dir(filename, x))

            else:
                if dirname is not None:
                    all_files.append(dirname + '/' + x)
                else:
                    all_files.append(x)
        return all_files

    def put_dir(self, local_dir, remote_dir):
        '''
        上传目录
        :param local_dir:
        :param remote_dir:
        :return:
        '''

        sftp = self.__ssh.open_sftp()

        # 去除远程路径最后的字符‘/’
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        all_files = self.__get_all_files_in_local_dir(local_dir)
        for x in all_files:
            filename = os.path.join(local_dir, x)
            remote_filename = remote_dir + '/' + x
            if os.path.isdir(filename):
                sftp.mkdir(remote_filename)
            else:
                print(' Put 文件{}传输中...'.format(filename))
                sftp.put(filename, remote_filename)
        sftp.close()

    def close(self):
        self.__ssh.close()
        print('关闭连接')

```



### SFTP工具类

```java
# -*- coding:utf-8 -*-
import os
import sys
from stat import S_ISDIR

import paramiko

class SFTPUtils(object):

    def __init__(self, server, user='root', password=None, port=22):
        '''
        初始化
        :param server: 服务器IP
        :param user: 用户名
        :param password: 用户密码
        :param port: 端口号
        '''
        self.user = user
        self.password = password
        self.server = server
        self.port = port
        self.__transport = None
        self.__sftp = None

    def connect(self):
        '''
        与服务器建立连接
        :return:
        '''
        try:
            self.__transport = paramiko.Transport((self.server, self.port))
            self.__transport.connect(username=self.user, password=self.password)
            self.__sftp = paramiko.SFTPClient.from_transport(self.__transport)
            print('SFTP 连接到服务器：成功')
        except Exception as e:
            print('连接到服务器：失败；{}', e.__str__())

    def put_file(self, local_file, remote_file):
        '''
        上传文件
        :param local_file:
        :param remote_file:
        :return:
        '''
        try:
            self.__sftp.put(local_file, remote_file)
            print("下载文件{}:成功".format(local_file))
        except Exception as e:
            print("上传文件{}:失败;{}".format(local_file, e.__str__()))

    def get_file(self, remote_file, local_file):
        '''
        上传文件
        :param local_file:
        :param remote_file:
        :return:
        '''
        try:
            self.__sftp.get(remote_file, local_file)
            print("下载文件{}:成功".format(remote_file))
        except Exception as e:
            print("下载文件{}:失败;{}".format(remote_file, e.__str__()))

    def __get_all_files_in_remote_dir(self, sftp, remote_dir, dirname=None):
        '''
        获取远程目录的所有文集
        :param sftp:
        :param remote_dir:
        :return:
        '''
        # 保存所有文件的列表
        all_files = list()

        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        files = sftp.listdir_attr(remote_dir)
        for x in files:
            filename = remote_dir + '/' + x.filename
            if S_ISDIR(x.st_mode):
                if dirname is not None:
                    all_files.append((dirname+'/'+x.filename, True))
                    all_files.extend(self.__get_all_files_in_remote_dir(sftp, filename, dirname+'/'+x.filename))
                else:
                    all_files.append((x.filename, True))
                    all_files.extend(self.__get_all_files_in_remote_dir(sftp, filename, x.filename))
            else:
                if dirname is not None:
                    all_files.append((dirname+'/'+x.filename, False))
                else:
                    all_files.append((x.filename, False))
        return all_files

    def get_dir(self, remote_dir, local_dir):
        '''
        下载目录
        :param remote_dir:
        :param local_dir:
        :return:
        '''
        try:
            sftp = self.__sftp
            all_files = self.__get_all_files_in_remote_dir(sftp, remote_dir)
            print('all_files:', all_files)
            for x, dir_flag in all_files:
                filename = x
                local_filename = os.path.join(local_dir, filename)
                if dir_flag:
                    os.mkdir(local_filename)
                else:
                    remote_file = remote_dir+'/'+x
                    print('Get文件{}传输中...'.format(remote_file))
                    sftp.get(remote_file, local_filename)
        except Exception as e:
            print("下载目录失败：", e.__str__())


    def __get_all_files_in_local_dir(self, local_dir, dirname=None):
        '''
        获取本地目录的所有文集
        :param local_dir:
        :return:
        '''
        # 保存所有文件的列表
        all_files = list()

        # if local_dir[-1] == '/':
        #     local_dir = local_dir[0:-1]

        # 获取本地目录的属性值
        files = os.listdir(local_dir)
        for x in files:
            filename = os.path.join(local_dir, x)
            # 如果是目录, 则递归处理该目录
            if os.path.isdir(filename):

                if dirname is not None:
                    all_files.append(dirname + '/' + x)
                    all_files.extend(self.__get_all_files_in_local_dir(filename, dirname +'/'+ x))
                else:
                    all_files.append(x)
                    all_files.extend(self.__get_all_files_in_local_dir(filename, x))

            else:
                if dirname is not None:
                    all_files.append(dirname + '/' + x)
                else:
                    all_files.append(x)
        return all_files

    def put_dir(self, local_dir, remote_dir):
        '''
        上传目录
        :param local_dir:
        :param remote_dir:
        :return:
        '''

        sftp = self.__sftp

        # 去除远程路径最后的字符‘/’
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        all_files = self.__get_all_files_in_local_dir(local_dir)
        for x in all_files:
            filename = os.path.join(local_dir, x)
            remote_filename = remote_dir + '/' + x
            if os.path.isdir(filename):
                sftp.mkdir(remote_filename)
            else:
                print(' Put 文件{}传输中...'.format(filename))
                sftp.put(filename, remote_filename)
        sftp.close()


    def close(self):
        self.__transport.close()
        print('SFTP关闭连接')
```


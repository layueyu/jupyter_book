# Scapy 介绍

PYTHON安装：

- `pip3 install scapy`

### 收发数据包

- sr() : 发送三层数据包，等待接收一个或者多个数据包的响应
- sr1() ：发送三层数据包，并仅仅只等待接收一个数据包的响应
- srp() ： 发送二层数据包，并且等待响应
- send() ： 仅仅发送三层数据包，系统会自动处理路由和二层信息
- sendp() ：发送二层数据包

#### Ping扫描


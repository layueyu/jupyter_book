# springboot 检索

- ElasticSearch 是目前全文搜索引擎的首选

- ElasticSearch  是一个分布式搜索服务，提供Restful API，地秤基于Lucene，采用多shard的方式保证数据安全

- 安装

  - docker 安装

    ```bash
    # 不使用加速器
    docker pull elasticsearch
    
    # 使用中国官方镜像加速器
    docker pull registry.docker-cn.com/library/elasticsearch
    ```

  - 运行

    ```bash
    docker run -e ES_JAVA_OPTS="-Xms256m -Xmx256m" -d -p 9200:9200 -p 9300:9300 --name ES01 映像名
    ```


### 整合ElasticSearch 

1. springboot默认支持两种技术来和ES交互

   1. Jest(默认不生效)；需要导入工具包（io.searchbox.client.JestClient）

      1. 导入

         ```xml
         <dependency>
             <groupId>io.searchbox</groupId>
             <artifactId>jest</artifactId>
             <version>5.3.3</version>
         </dependency>
         ```

      2. 配置

         ```yml
         spring:
           elasticsearch:
             jest:
               uris: http://192.168.0.147:9200 # 服务器路径
         ```

   2. SpringData ElasticSearch

      1. 引入

         ```xml
         <dependency>
             <groupId>org.springframework.boot</groupId>
             <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
         </dependency>
         ```

      2. 配置；Client;  节点信息 clusterNodes;clusterName

         ```yml
           data:
             elasticsearch:
               cluster-name: elasticsearch
               cluster-nodes: 192.168.0.147:9300
         ```

      3. ElasticSearchTemplate 操作es

      4. 编写一个ElasticSearchRepository的子接口来操作ES

      5. 两种用法

         - 帮助文档：https://github.com/spring-projects/spring-data-elasticsearch



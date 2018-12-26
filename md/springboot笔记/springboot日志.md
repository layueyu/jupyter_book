# Spring boot  logback 基础使用篇

## 1.简单日志配置

### 1.1配置控制台日志的debug级别

- spring boot 默认情况下，从控制台打印出来的日志级别只有ERROR、WARN还有INFO；想打印debug级别的，可以在application.properites配置debug=true

  ```yml
  debug=true
  ```

###1.2 在生产环境下，你可以通过命令配置日志的debug级别

- ```bash
  java -jar demo.jar --debug
  ```

### 1.3 配置logging.level.*来具体输出那些包的日志级别

- ```yml
  logging.level.root=INFO
  logging.level.org.springframework.web=DEBUG
  logging.level.org.hibernate=ERROR
  ```

### 1.4 将日志输出到文件中

- 默认：spring boot是不将日志输出到日志文件中；可以在application.properite文件中配置logging.file文件名称和logging.path文件路径，将日志输出到文件中

  ```yml
  logging.path=F:\\demo
  logging.file=demo.log
  logging.level.root=info
  ```

  注：

  - 这里若不配置具体的包的日志级别，日志文件信息将为空

  - 若只配置logging.path，那么将会在F:\demo文件夹生成一个日志文件为spring.log（ps：该文件名是固定的，不能更改）。如果path路径不存在，会自动创建该文件夹

  - 若只配置logging.file，那将会在项目的当前路径下生成一个demo.log日志文件。这里可以使用绝对路径如，会自动在e盘下创建文件夹和相应的日志文件。

    ```yml
    logging.file=e:\\demo\\demo.log
    ```

  - logging.path和logging.file同时配置，不会在这个路径有F:\demo\demo.log日志生成，logging.path和logging.file不会进行叠加（要注意）

  - logging.path和logging.file的value都可以是相对路径或者绝对路径

## 2. logback的介绍及配置

### 2.1 logback的介绍

- Logback是由log4j创始人设计的又一个开源日志组件。
- logback当前分成三个模块：logback-core,logback-classic和logback-access。
  - logback-core是其它两个模块的基础模块。
  - logback-classic是log4j的一个改良版本。此外logback-classic完整实现[SLF4J API](http://www.oschina.net/p/slf4j)使你可以很方便地更换成其它日志系统如log4j或JDK14 Logging。logback-access访问模块与Servlet容器集成提供通过Http来访问日志的功能。

### 2.2 logback取代log4j的理由：

- **更快的实现** ；logback不仅性能提升了，初始化内存加载也更小了
- **非常充分的测试**  ；Logback的测试完全不同级别的
- **Logback-classic非常自然实现了SLF4j**
- **非常充分的文档**  
- **自动重新加载配置文件**  
- **Lilith**   
- **谨慎的模式和非常友好的恢复**  
- **配置文件可以处理不同的情况**   
- **Filters**
- **SiftingAppender（一个非常多功能的Appender）**  它可以用来分割日志文件根据任何一个给定的运行参数
- **自动压缩已经打出来的log**  RollingFileAppender在产生新文件的时候，会自动压缩已经打出来的日志文件。压缩是个异步过程，所以甚至对于大的日志文件，在压缩过程中应用不会受任何影响
- **堆栈树带有包版本**  Logback在打出堆栈树日志时，会带上包的数据
- **自动去除旧的日志文件**  通过设置TimeBasedRollingPolicy或者SizeAndTimeBasedFNATP的maxHistory属性，你可以控制已经产生日志文件的最大数量。如果设置maxHistory 12，那那些log文件超过12个月的都会被自动移除。

### 2.3 Logback的配置介绍

- **1、Logger、appender及layout**
  - Logger 作为日志的记录器，把它关联到应用的对应的context上后，主要用于存放日志对象，也可以定义日志类型、级别
  - Appender 主要用于指定日志输出的目的地，目的地可以是控制台、文件、远程套接字服务器、MySQL、PostreSQL、Oracle和其他数据库、JMS和远程UNIX Syslog守护进程
  - Layout 负责把事件转换成字符串，格式化的日志信息的输出
- **2、logger context**
  - 各个logger都被关联到一个LoggerContext，LoggerContext负责制造logger，也负责以树结构排列各 logger。其他所有logger也通过org.slf4j.LoggerFactory 类的静态方法getLogger取得。 getLogger方法以 logger 名称为参数。用同一名字调用LoggerFactory.getLogger 方法所得到的永远都是同一个logger对象的引用。
- **3、有效级别及级别的继承**
  -  Logger 可以被分配级别。级别包括：TRACE、DEBUG、INFO、WARN 和ERROR，定义于 ch.qos.logback.classic.Level类。如果 logger没有被分配级别，那么它将从有被分配级别的最近的祖先那里继承级别。root logger 默认级别是 DEBUG。
- **4、打印方法与基本的选择规则**
  - **该规则是 logback 的核心。级别排序为： TRACE < DEBUG < INFO < WARN < ERROR。** 

### 3 logback的使用

#### 3.1 Logback的默认配置

- **1、Logback的配置文件**

  - Logback 配置文件的语法非常灵活。配置文件的基本结构：以`<configuration>`开头，后面有零个或多个`<appender>`元素，有零个或多个`<logger>`元素，有最多一个`<root>`元素

- **2、Logback默认配置的步骤**

  - 尝试在 classpath 下查找文件 logback-test.xml；
  - 如果文件不存在，则查找文件 logback.xml；
  - 如果两个文件都不存在，logback 用 Bas icConfigurator 自动对自己进行配置，这会导致记录输出到控制台。

- **3、Logback.xml 文件** 

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <!--
      Copyright 2010-2011 The myBatis Team
      Licensed under the Apache License, Version 2.0 (the "License");
      you may not use this file except in compliance with the License.
      You may obtain a copy of the License at
          http://www.apache.org/licenses/LICENSE-2.0
      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
      See the License for the specific language governing permissions and
      limitations under the License.
  -->
  <configuration debug="false">
      <!--定义日志文件的存储地址 勿在 LogBack 的配置中使用相对路径-->  
      <property name="LOG_HOME" value="/home" />  
      <!-- 控制台输出 -->   
      <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
          <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder"> 
               <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符--> 
              <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n</pattern>   
          </encoder> 
      </appender>
      <!-- 按照每天生成日志文件 -->   
      <appender name="FILE"  class="ch.qos.logback.core.rolling.RollingFileAppender">   
          <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
              <!--日志文件输出的文件名-->
              <FileNamePattern>${LOG_HOME}/TestWeb.log.%d{yyyy-MM-dd}.log</FileNamePattern> 
              <!--日志文件保留天数-->
              <MaxHistory>30</MaxHistory>
          </rollingPolicy>   
          <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder"> 
              <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符--> 
              <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n</pattern>   
          </encoder> 
          <!--日志文件最大的大小-->
         <triggeringPolicy class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy">
           <MaxFileSize>10MB</MaxFileSize>
         </triggeringPolicy>
      </appender> 
     <!-- show parameters for hibernate sql 专为 Hibernate 定制 --> 
      <logger name="org.hibernate.type.descriptor.sql.BasicBinder"  level="TRACE" />  
      <logger name="org.hibernate.type.descriptor.sql.BasicExtractor"  level="DEBUG" />  
      <logger name="org.hibernate.SQL" level="DEBUG" />  
      <logger name="org.hibernate.engine.QueryParameters" level="DEBUG" />
      <logger name="org.hibernate.engine.query.HQLQueryPlan" level="DEBUG" />  
      
      <!--myibatis log configure--> 
      <logger name="com.apache.ibatis" level="TRACE"/>
      <logger name="java.sql.Connection" level="DEBUG"/>
      <logger name="java.sql.Statement" level="DEBUG"/>
      <logger name="java.sql.PreparedStatement" level="DEBUG"/>
      
      <!-- 日志输出级别 -->
      <root level="INFO">
          <appender-ref ref="STDOUT" />
          <appender-ref ref="FILE" />
      </root> 
       <!--日志异步到数据库 -->  
      <appender name="DB" class="ch.qos.logback.classic.db.DBAppender">
          <!--日志异步到数据库 --> 
          <connectionSource class="ch.qos.logback.core.db.DriverManagerConnectionSource">
             <!--连接池 --> 
             <dataSource class="com.mchange.v2.c3p0.ComboPooledDataSource">
                <driverClass>com.mysql.jdbc.Driver</driverClass>
                <url>jdbc:mysql://127.0.0.1:3306/databaseName</url>
                <user>root</user>
                <password>root</password>
              </dataSource>
          </connectionSource>
    </appender>
  </configuration>
  ```

#### 3.2 在程序应用引用Logback

```java
package com.stu.system.action; 

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class BlogAction{
     //定义一个全局的记录器，通过LoggerFactory获取
     private final static Logger logger = LoggerFactory.getLogger(BlogAction.class); 
     /**
     * @param args
     */
    public static void main(String[] args) {
        logger.info("logback 成功了");
        logger.error("logback 成功了");
    }
}
```

### 4. logback.xml 配置示例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!--
       说明：
       1、日志级别及文件
           日志记录采用分级记录，级别与日志文件名相对应，不同级别的日志信息记录到不同的日志文件中
           例如：error级别记录到log_error_xxx.log或log_error.log（该文件为当前记录的日志文件），而log_error_xxx.log为归档日志，
           日志文件按日期记录，同一天内，若日志文件大小等于或大于2M，则按0、1、2...顺序分别命名
           例如log-level-2013-12-21.0.log
           其它级别的日志也是如此。
       2、文件路径
           若开发、测试用，在Eclipse中运行项目，则到Eclipse的安装路径查找logs文件夹，以相对路径../logs。
           若部署到Tomcat下，则在Tomcat下的logs文件中
       3、Appender
           FILEERROR对应error级别，文件名以log-error-xxx.log形式命名
           FILEWARN对应warn级别，文件名以log-warn-xxx.log形式命名
           FILEINFO对应info级别，文件名以log-info-xxx.log形式命名
           FILEDEBUG对应debug级别，文件名以log-debug-xxx.log形式命名
           stdout将日志信息输出到控制上，为方便开发测试使用
    -->
    <contextName>SpringBootDemo</contextName>
    <property name="LOG_PATH" value="D:\\JavaWebLogs" />
    <!--设置系统日志目录-->
    <property name="APPDIR" value="SpringBootDemo" />

    <!-- 日志记录器，日期滚动记录 -->
    <appender name="FILEERROR" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!-- 正在记录的日志文件的路径及文件名 -->
        <file>${LOG_PATH}/${APPDIR}/log_error.log</file>
        <!-- 日志记录器的滚动策略，按日期，按大小记录 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- 归档的日志文件的路径，例如今天是2013-12-21日志，当前写的日志文件路径为file节点指定，可以将此文件与file指定文件路径设置为不同路径，从而将当前日志文件或归档日志文件置不同的目录。
            而2013-12-21的日志文件在由fileNamePattern指定。%d{yyyy-MM-dd}指定日期格式，%i指定索引 -->
            <fileNamePattern>${LOG_PATH}/${APPDIR}/error/log-error-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <!-- 除按日志记录之外，还配置了日志文件不能超过2M，若超过2M，日志文件会以索引0开始，
            命名日志文件，例如log-error-2013-12-21.0.log -->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>2MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
        </rollingPolicy>
        <!-- 追加方式记录日志 -->
        <append>true</append>
        <!-- 日志文件的格式 -->
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <pattern>===%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level %logger Line:%-3L - %msg%n</pattern>
            <charset>utf-8</charset>
        </encoder>
        <!-- 此日志文件只记录info级别的 -->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>error</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <!-- 日志记录器，日期滚动记录 -->
    <appender name="FILEWARN" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!-- 正在记录的日志文件的路径及文件名 -->
        <file>${LOG_PATH}/${APPDIR}/log_warn.log</file>
        <!-- 日志记录器的滚动策略，按日期，按大小记录 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- 归档的日志文件的路径，例如今天是2013-12-21日志，当前写的日志文件路径为file节点指定，可以将此文件与file指定文件路径设置为不同路径，从而将当前日志文件或归档日志文件置不同的目录。
            而2013-12-21的日志文件在由fileNamePattern指定。%d{yyyy-MM-dd}指定日期格式，%i指定索引 -->
            <fileNamePattern>${LOG_PATH}/${APPDIR}/warn/log-warn-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <!-- 除按日志记录之外，还配置了日志文件不能超过2M，若超过2M，日志文件会以索引0开始，
            命名日志文件，例如log-error-2013-12-21.0.log -->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>2MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
        </rollingPolicy>
        <!-- 追加方式记录日志 -->
        <append>true</append>
        <!-- 日志文件的格式 -->
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <pattern>===%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level %logger Line:%-3L - %msg%n</pattern>
            <charset>utf-8</charset>
        </encoder>
        <!-- 此日志文件只记录info级别的 -->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>warn</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <!-- 日志记录器，日期滚动记录 -->
    <appender name="FILEINFO" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!-- 正在记录的日志文件的路径及文件名 -->
        <file>${LOG_PATH}/${APPDIR}/log_info.log</file>
        <!-- 日志记录器的滚动策略，按日期，按大小记录 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- 归档的日志文件的路径，例如今天是2013-12-21日志，当前写的日志文件路径为file节点指定，可以将此文件与file指定文件路径设置为不同路径，从而将当前日志文件或归档日志文件置不同的目录。
            而2013-12-21的日志文件在由fileNamePattern指定。%d{yyyy-MM-dd}指定日期格式，%i指定索引 -->
            <fileNamePattern>${LOG_PATH}/${APPDIR}/info/log-info-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <!-- 除按日志记录之外，还配置了日志文件不能超过2M，若超过2M，日志文件会以索引0开始，
            命名日志文件，例如log-error-2013-12-21.0.log -->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>2MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
        </rollingPolicy>
        <!-- 追加方式记录日志 -->
        <append>true</append>
        <!-- 日志文件的格式 -->
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <pattern>===%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level %logger Line:%-3L - %msg%n</pattern>
            <charset>utf-8</charset>
        </encoder>
        <!-- 此日志文件只记录info级别的 -->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>info</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <!--encoder 默认配置为PatternLayoutEncoder-->
        <encoder>
            <pattern>===%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level %logger Line:%-3L - %msg%n</pattern>
            <charset>utf-8</charset>
        </encoder>
        <!--此日志appender是为开发使用，只配置最底级别，控制台输出的日志级别是大于或等于此级别的日志信息-->
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>debug</level>
        </filter>
    </appender>

    <logger name="org.springframework" level="WARN" />
    <logger name="org.hibernate" level="WARN" />

    <!-- 生产环境下，将此级别配置为适合的级别，以免日志文件太多或影响程序性能 -->
    <root level="INFO">
        <appender-ref ref="FILEERROR" />
        <appender-ref ref="FILEWARN" />
        <appender-ref ref="FILEINFO" />

        <!-- 生产环境将请stdout,testfile去掉 -->
        <appender-ref ref="STDOUT" />
    </root>
</configuration>
```

### 5. 节点属性

#### 1、根节点`<configuration>`属性

- scan:

  - 当此属性设置为true时，配置文件如果发生改变，将会被重新加载，默认值为true

- scanPeriod

  - 设置监测配置文件是否有修改的时间间隔，若果没有给出时间单位，默认时毫秒。当scan为true时，此属性生效。默认的时间间隔为1分钟

- debug

  - 当此属性设置为true时，将打印出logback内部日志信息，实时查看logback运行状态，默认值false

  - 例如：

    ```xml
    <configuration scan="true" scanPeriod="60 seconds" debug="false">
          <!-- 其他配置省略-->
    </configuration>
    ```

#### 2、根节点`<configuration>`的子节点

- appender
- logger
- root

##### 2.1 设置上下文名称：`<contextName>`

- 每个logger都关联到logger上下文，默认上下文名称为“default”

- 使用<contextName>设置成其他名字，用于区分不同应用程序的记录。一旦设置，不能修改

  ```xml
  <configuration scan="true" scanPeriod="60 seconds" debug="false">
        <contextName>myAppName</contextName>
        <!-- 其他配置省略-->
  </configuration>
  ```

##### 2.2 设置变量：`<property>`

- 用来定义变量值的标签，

- `<property>` 有两个属性，name和value；

  - 其中name的值是变量的名称，value的值时变量定义的值。

  - 通过`<property>`定义的值会被插入到logger上下文中。定义变量后，可以使“${}”来使用变量。

  - ```xml
    <configuration scan="true" scanPeriod="60 seconds" debug="false">
          <property name="APP_Name" value="myAppName" /> 
          <contextName>${APP_Name}</contextName>
          <!-- 其他配置省略-->
    </configuration> 
    ```

##### 2.3 获取时间戳字符串：`<timestamp>`

- 两个属性：

  - key: 标识此`<timestamp>` 的名字；

  - datePattern：设置将当前时间（解析配置文件的时间）转换为字符串的模式，遵循java.txt.SimpleDateFormat的格式

  - ```xml
    <configuration scan="true" scanPeriod="60 seconds" debug="false">
          <timestamp key="bySecond" datePattern="yyyyMMdd'T'HHmmss"/> 
          <contextName>${bySecond}</contextName>
          <!-- 其他配置省略-->
    </configuration>  
    ```

##### 2.4 设置loger节点

- `<loger>`
  - 用来设置某一个包或者具体的某一个类的日志打印级别、以及指定`<appender>`。`<loger>`仅有一个name属性，一个可选的level和一个可选的addtivity属性。
  - name: 
    - 用来指定受此loger约束的某一个包或者具体的某一个类。
  - level:
    - 用来设置打印级别，大小写无关：TRACE, DEBUG, INFO, WARN, ERROR, ALL 和 OFF，还有一个特殊值INHERITED或者同义词NULL，代表强制执行上级的级别。
    - 总结下各个节点的优先级：root<append<loger
  - addtivity
    - 是否向上级loger传递打印信息。默认是true。

##### 2.5 设置root节点

- `<root>`

  - 只有一个level属性，应为已经被命名为"root".
  - level
    - 用来设置打印级别，大小写无关：TRACE, DEBUG, INFO, WARN, ERROR, ALL 和 OFF，不能设置为INHERITED或者同义词NULL。
    - 默认是DEBUG
  - `<root>`可以包含零个或多个`<appender-ref>`元素，标识这个appender将会添加到这个loger

- 配置文件

  - 只配置root

    ```xml
    <configuration> 
     
      <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender"> 
        <!-- encoder 默认配置为PatternLayoutEncoder --> 
        <encoder> 
          <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern> 
        </encoder> 
      </appender> 
     
      <root level="INFO">           
        <appender-ref ref="STDOUT" /> 
      </root>   
       
     </configuration>
    ```

  - 带有loger的配置，不指定级别，不指定appender

    ```xml
    <configuration> 
     
      <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender"> 
        <!-- encoder 默认配置为PatternLayoutEncoder --> 
        <encoder> 
          <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern> 
        </encoder> 
      </appender> 
     
      <!-- logback为java中的包 --> 
      <logger name="logback"/> 
     
      <root level="DEBUG">           
        <appender-ref ref="STDOUT" /> 
      </root>   
       
     </configuration>
    ```

  - 带有多个loger的配置，指定级别，指定appender

    ```xml
    <configuration> 
       <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender"> 
        <!-- encoder 默认配置为PatternLayoutEncoder --> 
        <encoder> 
          <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern> 
        </encoder> 
      </appender> 
     
      <!-- logback为java中的包 --> 
      <logger name="logback"/> 
      <!--logback.LogbackDemo：类的全路径 --> 
      <logger name="logback.LogbackDemo" level="INFO" additivity="false">
          <appender-ref ref="STDOUT"/>
      </logger> 
      
      <root level="ERROR">           
        <appender-ref ref="STDOUT" /> 
      </root>   
    </configuration>
    ```

##### 2.6 设置 appender

- `<appender>`是`<configuration>`的子节点，是负责写日志的组件。

- `<appender>`有两个必要属性name和class。name指定appender名称，class指定appender的全限定名。

- ConsoleAppender

  - 把日志添加到控制台，有以下子节点：

    - `<encoder>`: 对日志进行格式化

    - `<target>`: 字符串 System.out 或者 System.err, 默认 System.out

    - 例如：

      ```xml
      <configuration>
      
        <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
          <encoder>
            <pattern>%-4relative [%thread] %-5level %logger{35} - %msg %n</pattern>
          </encoder>
        </appender>
      
        <root level="DEBUG">
          <appender-ref ref="STDOUT" />
        </root>
      </configuration>
      ```

- FileAppender

  - 把日志添加到文件，有以下子节点：

    - `<file>`: 被写入文件名，可以是相对目录，也可以是绝对目录。如果上级目录不存在会自动创建，没有默认值

    - `<append>`: 如果是true，日志被追加到文件结尾，若果是false，清空现存文件，默认是true

    - `<encoder>`: 对记录事件进行格式化

    - `<prudent>`: 如果是true，日志会被安全的写入文件，即使其他FileAppender也在向此文件做写入操作，效率低，默认是 false。

    - 例如：

      ```xml
      <configuration>
      
        <appender name="FILE" class="ch.qos.logback.core.FileAppender">
          <file>testFile.log</file>
          <append>true</append>
          <encoder>
            <pattern>%-4relative [%thread] %-5level %logger{35} - %msg%n</pattern>
          </encoder>
        </appender>
              
        <root level="DEBUG">
          <appender-ref ref="FILE" />
        </root>
      </configuration>
      ```

- RollingFileAppender

  - 滚动记录文件，先将日志记录到指定文件，当符合某个条件时，将日志记录到其他文件。有以下子节点：

    - `<file>`:被写入的文件名，可以是相对目录，也可以是绝对目录，如果上级目录不存在会自动创建，没有默认值。
    - `<append>`: 如果是 true，日志被追加到文件结尾，如果是 false，清空现存文件，默认是true。
    - `<encoder>`: 对记录事件进行格式化
    - `<rollingPolicy>`: 当发生滚动时，决定 **RollingFileAppender** 的行为，涉及文件移动和重命名
    - `<triggeringPolicy >`: 告知 **RollingFileAppender** 何时激活滚动
    - `<prudent>`：当为true时，不支持FixedWindowRollingPolicy。支持TimeBasedRollingPolicy，但是有两个限制，1不支持也不允许文件压缩，2不能设置file属性，必须留空

  - rollingPolicy

    - TimeBasedRollingPolicy: 最常用的滚动策略，它根据时间来制定滚动策略，既负责滚动也负责出发滚动。有以下子节点
      - `<fileNamePattern>`:必要节点，包含文件名及“%d”转换符， “%d”可以包含一个`java.text.SimpleDateFormat指定的时间格式，如：%d{yyyy-MM}。如果直接使用 %d，默认格式是 yyyy-MM-dd。`**RollingFileAppender** 的file字节点可有可无，通过设置file，可以为活动文件和归档文件指定不同位置，当前日志总是记录到file指定的文件（活动文件），活动文件的名字不会改变；如果没设置file，活动文件的名字会根据**fileNamePattern** 的值，每隔一段时间改变一次。“/”或者“\”会被当做目录分隔符。 
      - `<maxHistory>`:可选节点，控制保留的归档文件的最大数量，超出数量就删除旧文件。假设设置每个月滚动，且`<maxHistory>`是6，则只保存最近6个月的文件，删除之前的旧文件。注意，删除旧文件是，那些为了归档而创建的目录也会被删除。
    - FixedWindowRollingPolicy： 根据固定窗口算法重命名文件的滚动策略。有以下子节点：
      - `<minIndex>`:窗口索引最小值
      - `<maxIndex>`:窗口索引最大值，当用户指定的窗口过大时，会自动将窗口设置为12。
      - `<fileNamePattern >`:必须包含“%i”例如，假设最小值和最大值分别为1和2，命名模式为 mylog%i.log,会产生归档文件mylog1.log和mylog2.log。还可以指定文件压缩选项，例如，mylog%i.log.gz 或者 没有log%i.log.zip

  - triggeringPolicy

    - **SizeBasedTriggeringPolicy：** 查看当前活动文件的大小，如果超过指定大小会告知**RollingFileAppender** 触发当前活动文件滚动。只有一个节点:

      - `<maxFileSize>`:这是活动文件的大小，默认值是10MB

      - 例如：

        ```xml
        <configuration> 
          <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender"> 
            
            <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy"> 
              <fileNamePattern>logFile.%d{yyyy-MM-dd}.log</fileNamePattern> 
              <maxHistory>30</maxHistory>  
            </rollingPolicy> 
         
            <encoder> 
              <pattern>%-4relative [%thread] %-5level %logger{35} - %msg%n</pattern> 
            </encoder> 
          </appender>  
         
          <root level="DEBUG"> 
            <appender-ref ref="FILE" /> 
          </root> 
        </configuration>
        ```

      - 例如：按照固定窗口模式生成日志文件，当文件大于20MB时，生成新的日志文件。窗口大小是1到3，当保存了3个归档文件后，将覆盖最早的日志。

        ```xml
        <configuration> 
          <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender"> 
            <file>test.log</file> 
         
            <rollingPolicy class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy"> 
              <fileNamePattern>tests.%i.log.zip</fileNamePattern> 
              <minIndex>1</minIndex> 
              <maxIndex>3</maxIndex> 
            </rollingPolicy> 
         
            <triggeringPolicy class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy"> 
              <maxFileSize>5MB</maxFileSize> 
            </triggeringPolicy> 
            <encoder> 
              <pattern>%-4relative [%thread] %-5level %logger{35} - %msg%n</pattern> 
            </encoder> 
          </appender> 
                 
          <root level="DEBUG"> 
            <appender-ref ref="FILE" /> 
          </root> 
        </configuration>
        ```

- 补充

  - 另外还有SocketAppender、SMTPAppender、DBAppender、SyslogAppender、SiftingAppender，并不常用

##### 2.7 设置 encoder

- 负责两件事，一是把日志信息转换成字节数组，二是把字节数组写入到输出流。

- 目前**PatternLayoutEncoder** 是唯一有用的且默认的**encoder** ，有一个<pattern>节点，用来设置日志的输入格式。使用“%”加“转换符”方式，如果要输出“%”，则必须用“\”对“\%”进行转义。

- 例如：

  ```xml
  <encoder> 
     <pattern>%-4relative [%thread] %-5level %logger{35} - %msg%n</pattern> 
  </encoder
  ```

- `<pattern>` 里面换行符说明

  - [参考文档](https://www.cnblogs.com/lixuwu/p/5811273.html)

- 格式修饰符和转换符结合

  - **格式修饰符，与转换符共同使用：**

    - 可选的格式修饰符位于“%”和转换符之间。

    - 第一个可选修饰符是**左对齐** 标志，符号是减号“-”；

    - 接着是可选的**最小宽度** 修饰符，用十进制数表示。如果字符小于最小宽度，则左填充或右填充，默认是左填充（即右对齐），填充符为空格。如果字符大于最小宽度，字符永远不会被截断。

    - **最大宽度** 修饰符，符号是点号"."后面加十进制数。如果字符大于最大宽度，则从前面截断。点符号“.”后面加减号“-”在加数字，表示从尾部截断。

    - 例如：%-4relative 表示，将输出从程序启动到创建日志记录的时间 进行左对齐 且最小宽度为4。

##### 2.8 filter的使用

- `<filter>`

  - Logback的过滤器基于三值逻辑（ternary  logic），允许把它们组装或成链，从而组成任意的复合过滤策略。过滤器很大程度上受到Linux的iptables启发。这里的所谓三值逻辑是说，过滤器的返回值只能是ACCEPT、DENY和NEUTRAL的其中一个。

    - 如果返回DENY，那么记录事件立即被抛弃，不再经过剩余过滤器；
    - 如果返回NEUTRAL，那么有序列表里的下一个过滤器会接着处理记录事件；
    - 如果返回ACCEPT，那么记录事件被立即处理，不再经过剩余过滤器。

    过滤器被添加到`<Appender>`中，为`<Appender>` 添加一个或多个过滤器后，可以用任意条件对日志进行过滤。`<Appender>` 有多个过滤器时，按照配置顺序执行。

- 常用的过滤器

  - **LevelFilter：** 级别过滤器，根据日志级别进行过滤。如果日志级别等于配置级别，过滤器会根据onMath 和 onMismatch接收或拒绝日志。有以下子节点：

    - `<level>`:设置过滤级别

    - `<onMatch>`:用于配置符合过滤条件的操作

    - `<onMismatch>`:用于配置不符合过滤条件的操作

    - 例如：将过滤器的日志级别配置为INFO，所有INFO级别的日志交给appender处理，非INFO级别的日志，被过滤掉。

      ```xml
      <configuration> 
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender"> 
          <filter class="ch.qos.logback.classic.filter.LevelFilter"> 
            <level>INFO</level> 
            <onMatch>ACCEPT</onMatch> 
            <onMismatch>DENY</onMismatch> 
          </filter> 
          <encoder> 
            <pattern> 
              %-4relative [%thread] %-5level %logger{30} - %msg%n 
            </pattern> 
          </encoder> 
        </appender> 
        <root level="DEBUG"> 
          <appender-ref ref="CONSOLE" /> 
        </root> 
      </configuration>
      ```

  - **ThresholdFilter：** 临界值过滤器，过滤掉低于指定临界值的日志。

    - 当日志级别等于或高于临界值时，过滤器返回NEUTRAL；当日志级别低于临界值时，日志会被拒绝

    - 例如：过滤掉所有低于INFO级别的日志。

      ```xml
      <configuration> 
        <appender name="CONSOLE" 
          class="ch.qos.logback.core.ConsoleAppender"> 
          <!-- 过滤掉 TRACE 和 DEBUG 级别的日志--> 
          <filter class="ch.qos.logback.classic.filter.ThresholdFilter"> 
            <level>INFO</level> 
          </filter> 
          <encoder> 
            <pattern> 
              %-4relative [%thread] %-5level %logger{30} - %msg%n 
            </pattern> 
          </encoder> 
        </appender> 
        <root level="DEBUG"> 
          <appender-ref ref="CONSOLE" /> 
        </root> 
      </configuration>
      ```

  - **EvaluatorFilter：** 求值过滤器，评估、鉴别日志是否符合指定条件。需要额外的两个JAR包，commons-compiler.jar和janino.jar有以下子节点：

    - [参考文档](https://www.cnblogs.com/lixuwu/p/5816814.html)
















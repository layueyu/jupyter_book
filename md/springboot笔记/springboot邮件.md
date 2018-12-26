# springboot邮件

### 引入依赖

- 引入 `spring-boot-starter-mail`

  ```xml
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-mail</artifactId>
  </dependency>
  ```

- 配置

  ```yml
  spring:
    mail:
      username: 123@qq.com
      password: bcphj # 密码或授权码
      host: smtp.qq.com
  ```

### 使用

- 简单邮件发送：SimpleMailMessage

- 复杂邮件发送

  ```java
  // 创建一个复杂的消息邮件
  MimeMessage mimeMessage = mailSender.createMimeMessage();
  MimeMessageHelper helper = new MimeMessageHelper(mimeMessage, true);
  
  // 邮件设置
  helper.setSubject("通知");
  helper.setText("测试通知");
  helper.setTo("123@qq.com");
  helper.setFrom("123@qq.com");
  
  // 上传附件
  helper.addAttachment("1.jpg",new File("C:\\Users\\zhuowen\\Downloads\\1.jpg"));
  
  mailSender.send(mimeMessage);
  ```



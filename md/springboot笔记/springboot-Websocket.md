# spring boot Websocket

- [WebSocket简介和spring boot 集成简单消息代理](https://juejin.im/post/5ac8cd5c6fb9a028dd4e7ba6)
- WebSocketMessageBrokerConfigurer
  - 配置消息代理，默认情况下使用内置的消息代理。类上的注解`@EnableWebSocketMessageBroker`：此注解表示使用STOMP协议来传输基于消息代理的消息，此时可以在`@Controller`类中使用`@MessageMapping`。
  - 在方法`registerStompEndpoints()`里`addEndpoint`方法：添加STOMP协议的端点。这个HTTP URL是供WebSocket或SockJS客户端访问的地址;`withSockJS`：指定端点使用SockJS协议
  - 在方法`configureMessageBroker()`里设置简单消息代理，并配置消息的发送的地址符合配置的前缀的消息才发送到这个broker

### 1. 引入starter

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

### 2. 编写配置类

```java
package io.renren.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

@Configuration
//注解开启使用STOMP协议来传输基于代理(message broker)的消息
//此时可以在@Controller使用@MessageMapping,就像使用@RequestMapping一样
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        /**
         * 注册 STOMP的端点
         * addEndpoint：这里设置的simple broker是指可以订阅的地址，也就是服务器可以发送的地址
         * withSockJS: 指定端点使用SockJS协议
         * setAllowedOrigins("*") 添加允许跨域访问
         */
        registry.addEndpoint("/websocket")
                .setAllowedOrigins("*");
//        .withSockJS();
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        /**
         * 配置消息代理
         * 启用简单Broker，消息的发送地址符合配置的前缀来的消息才发送到这个broker
         * 设置接收客户端订阅 的 路径前缀（必须不设置，可以为空串）
         */
        registry.enableSimpleBroker("/topic");
    }
}
```

### 3.使用

```java
@Autowired
private SimpMessagingTemplate simpMessagingTemplate; 

.....
    
simpMessagingTemplate.convertAndSend("/topic/demo", "123:-->");
```


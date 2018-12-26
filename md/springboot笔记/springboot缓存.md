# spring boot 缓存

|                | 说明                           |
| -------------- | ---------------------------- |
| Cache          | 缓存接口，定义缓存操作。实现有：RedisCache等  |
| CacheManager   | 缓存管理器，管理各种缓存（Cache）组件        |
| @Cacheable     | 主要针对方法配置，能够根据方法的请求参数对其结果进行缓存 |
| @CacheEvict    | 清空缓存                         |
| @CachePut      | 保证方法被调用，有希望结果被缓存             |
| @EnableCaching | 开启基于注解的缓存                    |
| keyGenerator   | 缓存数据时key的生成策略                |
| serialize      | 缓存数据时value序列化策略              |

## @Cacheable

#### 属性

- cacheNames/value 指定缓存组件的名字；将方法的返回结果放在那个缓存中，是数组的方式，可以指定多个缓存

- key： 缓存数据使用的key；可以用他来指定。默认使用方法的参数值，可使用SPEL表达式；

- keyGenerator ： key的生成器，可以自己指定key的生成器的组件id；与key属性二选一

- cacheManager： 指定缓存管理器

- cacheResolver:  指定缓存解析器；与cacheManager二选一

- condition: 指定符合条件的情况下才缓存，例如:condition="#id>0"

- unless： 否定缓存，当unless指定的条件为true，方法返回的值就不会被缓存；可以获取到结果进行判断

- sync： 是否使用异步模式;在此模式下不支持unless

- ##### SPEL表达式

  | 名字            | 位置                 | 描述                                       | 示例                    |
  | ------------- | ------------------ | ---------------------------------------- | --------------------- |
  | methodName    | root object        | 当前被调用的方法名                                | `#root.methodName`    |
  | method        | root object        | 当前被调用的方法                                 | `#root.method.namer`  |
  | target        | root object        | 当前被调用的目标对象                               | `#root.target`        |
  | targetClass   | root object        | 当前被调用的目标对象类                              | `#root.targetClass`   |
  | args          | root object        | 当前被调用的参数列表                               | `#root.args[0]`       |
  | caches        | root object        | 当前方法调用使用的缓存列表（如@Cacheable(value={"cache1","cache2"})）,则有两个cache | `#root.cache[0].name` |
  | argument name | evaluation context | 方法参数的名字，可以直接使用#参数名，也可以使用#p0或#a0的形式，0代表参数的索引 | `#iban、#a0、#p0`       |
  | result        | evaluation context | 方法执行后的返回值（仅方法执行后的判断有效，如‘unless’，‘cache put’的表达式 ‘cache evict’的表达式 beforeinvocation=false） | `#result`             |


##### 说明：

- 方法执行之前先检查缓存中有没有这个数据，默认按照参数的值作为key去查询缓存，如果没有就运行方法并将结果放入缓存;以后再次调用可以直接使用缓存中的数据

- 默认使用SimpleKeyGenerator生成key，其默认策略：
  - 没有参数；key = new SimpleKey()
  - 若果有一个参数：key = 参数的值
  - 若果有多个参数：key = new SimpleKey(params)

- 默认使用CacheManager[ConcurrentMapCacheManager]按照名字得到cache[ConcurrentMapCache]组件

- 自定义KeyGenerator：

  ```java
  // import org.springframework.cache.interceptor.KeyGenerator;
  
  @Bean("myKeyGenerator")
   public KeyGenerator keyGenerator(){
         return  new KeyGenerator(){
             @Override
             public Object generate(Object o, Method method, Object... objects) {
                 return method.getName()+"["+ Arrays.asList(objects)+"]";
             }
         };
   }
  ```



## @CachePut

#### 说明

- 即调用方法，又更新缓存数据；同步更新缓存（取缓存的key，与放缓存的key相同）；
- 运行时机：先调用方法，在目标方法的结果进行缓存



## @CacheEvict

#### 说明

- allEntries： 默认false；为true删除缓存中所有的数据
- beforeInvocation: 默认false，在方法之后执行，若出现异常缓存不会清除；为true缓存的清除是否在方法之前执行，无论方法是否出现异常缓存都会清除

## @Caching

#### 说明

- 是Cacheable、CachePut、CacheEvict的组合
- 可定义复杂的缓存规则



## @CaCheConfig

#### 说明

- 抽取缓存的公共配置

## 缓存中间件

### 整合redis

#### 1. 引入starter

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

#### 2. 配置redis

- yml 配置

  ```yml
  spring:
    redis:
      host: localhost #redis服务器IP
      port: 6379 #redis端口号
  ```

- 说明：

  - StringRedisTemplate: 操作k-v都是字符串

    ```java
    stringRedisTemplate.opsForValue(); //String 字符串
    stringRedisTemplate.opsForList();  //List 集合
    stringRedisTemplate.opsForSet();   //Set 集合
    stringRedisTemplate.opsForHash();  //Hash 散列
    stringRedisTemplate.opsForZSet();  //ZSet 有序集合
    ```

  - RedisTemplate: 操作k-v都是对象

#### 原理

1. 引入redis的starter，容器中保存的是 RedisCacheManager
2. RedisCacheManager 帮我们创建 RedisCache来作为缓存组件；RedisCache通过操作redis缓存数据
3. 默认保存数据k-v都是Object；利用序列化保存；如何保存为json
   1. 引入redis的starter，cacheManager变为RedisCacheManager
   2. 默认创建的RedisCacheManager 操作redis的时候使用的是 RedisTemplate<object,object>
   3. RedisTemplate<object,object>是默认使用jdk序列化机制
   4. 自定义CacheManager








## 使用redis实现分布式锁

- redis分布式锁是通过setnx命令实现的。该命令的作用是，当往redis中存入一个值时，会先判断该值对应的key是否存在，如果存在则返回0，如果不存在，则将该值存入redis并返回1。根据这个特性，我们在程序中，每次都调用setIfAbsent(该方法是setnx命令的实现)方法，来模拟是否获取到锁，如果返回true，则说明该key值不存在，表示获取到锁；如果返回false，则说明该key值存在，已经有程序在使用这个key值了，从而实现了类似加锁的功能。

- 示例

  ```java
  @Async("defaultTaskExecutor")
  public void testRedisClock(String name){
      log.info("进入线程");
      Boolean flag = false;
      try {
          flag = redisUtils.setIfAbsent(redis_clock_key,redis_clock_velue);
          if(flag){
              log.info("获取到分布式锁:{}",name);
              TimeUnit.SECONDS.sleep(1);
          }else {
              log.info("没有获取到分布式锁:{}",name);
          }
      } catch (Exception e) {
          log.info("异常：{}",e.getMessage());
      } finally {
          if(flag){
              redisUtils.delete(redis_clock_key);
              log.info("释放分布式锁:{}",name);
          }
      }
  }
  ```

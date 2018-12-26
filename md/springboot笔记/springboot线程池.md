# 异步任务线程池
- 在Springboot中对其进行了简化处理，只需要配置一个类型为java.util.concurrent.TaskExecutor或其子类的bean，并在配置类或直接在程序入口类上声明注解@EnableAsync。

- 调用也简单，在由Spring管理的对象的方法上标注注解@Async，显式调用即可生效。

- 一般使用Spring提供的ThreadPoolTaskExecutor类。

## 基本使用

- 创建配置类，ThreadPoolConfig.java

  ```java
  package io.renren.config;
  
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  import org.springframework.core.task.TaskExecutor;
  import org.springframework.scheduling.annotation.EnableAsync;
  import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
  
  import java.util.concurrent.ThreadPoolExecutor;
  
  /**
   * 线程池配置类
   *
   */
  @Configuration
  @EnableAsync //启用异步处理方式
  public class ThreadPoolConfig {
      @Bean(name = "defaultTaskExecutor")
      public TaskExecutor defaultTaskExecutor(){
          ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
          // 设置核心线程数
          executor.setCorePoolSize(5);
          // 设置最大线程数
          executor.setMaxPoolSize(10);
          // 设置队列容量
          executor.setQueueCapacity(20);
          // 设置线程活跃时间（秒）
          executor.setKeepAliveSeconds(60);
          // 设置默认线程名称前缀
          executor.setThreadNamePrefix("defaultTE-");
          // 设置拒绝策略
          // rejection-policy：当pool已经达到max size的时候，如何处理新任务
          // CALLER_RUNS：不在新线程中执行任务，而是有调用者所在的线程来执行
          executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
          // 等待所有任务结束后再关闭线程池
          executor.setWaitForTasksToCompleteOnShutdown(true);
          //执行初始化
          executor.initialize();
          return executor;
      }
  }
  ```

- 创建 service,

  ```java
  package io.renren.modules.hello.service;
  
  import org.slf4j.Logger;
  import org.slf4j.LoggerFactory;
  import org.springframework.scheduling.annotation.Async;
  import org.springframework.stereotype.Service;
  
  @Service
  public class HelloService {
  
      Logger log = LoggerFactory.getLogger(HelloService.class);
  
      @Async("defaultTaskExecutor")
      public void  sayHello(String name){
          log.info("线程测试--》{}",name);
      }
  }
  
  ```

- 使用,编写测试类

  ```java
  package io.renren;
  
  import io.renren.modules.hello.service.HelloService;
  import org.junit.Test;
  import org.junit.runner.RunWith;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.boot.test.context.SpringBootTest;
  import org.springframework.test.context.junit4.SpringRunner;
  
  @RunWith(SpringRunner.class)
  @SpringBootTest
  public class ThreadPoolTest {
  
      @Autowired
     private HelloService helloService;
  
      @Test
      public void test01(){
          for (int i = 0; i< 5; i++){
              helloService.sayHello(i+"");
          }
      }
  }
  ```


## 进阶

- 有时候我们不止希望异步执行任务，还希望任务执行完成后会有一个返回值，在java中提供了Future泛型接口，用来接收任务执行结果，springboot也提供了此类支持，使用实现了ListenableFuture接口的类如AsyncResult来作为返回值的载体。比如上例中，我们希望返回一个类型为String类型的值，可以将返回值改造为:

```java
@Async("defaultTaskExecutor")
public ListenableFuture<String> sayName(String name){
    try {
        log.info("带返回值线程测试-->{}",name);
        // 线程延时
        TimeUnit.SECONDS.sleep(10);
        String rest = name+" hello!";
        return new AsyncResult<>(rest);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return new AsyncResult<>("");
}
```

- 调用返回值

```java
@Test
public void test02(){
    try {
        for (int i = 0; i< 5; i++) {
            // 普通调用
            //                String s = helloService.sayName(i + "").get();
            // 限时调用
            String s = helloService.sayName(i + "").get(1, TimeUnit.SECONDS);
            System.out.println(s);
        }
    } catch (InterruptedException e) {  //中断异常
        e.printStackTrace();
    } catch (ExecutionException e) {
        e.printStackTrace();
    } catch (TimeoutException e) { //超时异常
        e.printStackTrace();
    }
}
```

## 扩展ThreadPoolTaskExecutor

- 虽然我们已经用上了线程池，但是还不清楚线程池当时的情况，有多少线程在执行，多少在队列中等待呢？这里我创建了一个ThreadPoolTaskExecutor的子类，在每次提交线程的时候都会将当前线程池的运行状况打印出来，代码如下：

  ```java
  package io.renren.config.ThreadPool.entity;
  
  import org.slf4j.Logger;
  import org.slf4j.LoggerFactory;
  import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
  import org.springframework.util.concurrent.ListenableFuture;
  
  import java.util.concurrent.Callable;
  import java.util.concurrent.Future;
  import java.util.concurrent.ThreadPoolExecutor;
  
  /**
   * 扩展ThreadPoolTaskExecutor
   */
  public class VisiableThreadPoolTaskExecutor extends ThreadPoolTaskExecutor{
      private static final Logger logger = LoggerFactory.getLogger(VisiableThreadPoolTaskExecutor.class);
  
      /**
       * 显示现称池信息
       * @param prefix
       */
      private void showThreadPoolInfo(String prefix){
          ThreadPoolExecutor threadPoolExecutor = getThreadPoolExecutor();
          if(null==threadPoolExecutor){ return; }
          logger.info("线程名称前缀：{}, 方法名:{}, 任务总数(taskCount):[{}], 结束任务的数量(completedTaskCount):[{}], 活跃数(activeCount):[{}], 等待数(queueSize)[{}]",
                  this.getThreadNamePrefix(),  // 线程名称前缀
                  prefix,
                  threadPoolExecutor.getTaskCount(),  //任务总数
                  threadPoolExecutor.getCompletedTaskCount(),  //结束任务的数量
                  threadPoolExecutor.getActiveCount(), // 活跃数
                  threadPoolExecutor.getQueue().size()); // 等待数
      }
  
      @Override
      public void execute(Runnable task) {
          showThreadPoolInfo("execute(Runnable task)");
          super.execute(task);
      }
  
      @Override public void execute(Runnable task, long startTimeout) {
          showThreadPoolInfo("execute(Runnable task, long startTimeout)");
          super.execute(task, startTimeout);
      }
  
      @Override public Future<?> submit(Runnable task) {
          showThreadPoolInfo("submit(Runnable task)");
          return super.submit(task);
      }
  
      @Override public <T> Future<T> submit(Callable<T> task) {
          showThreadPoolInfo("submit(Callable<T> task)");
          return super.submit(task);
      }
  
      @Override
      public ListenableFuture<?> submitListenable(Runnable task) {
          showThreadPoolInfo("submitListenable(Runnable task)");
          return super.submitListenable(task);
      }
  
      @Override public <T> ListenableFuture<T> submitListenable(Callable<T> task) {
          showThreadPoolInfo("submitListenable(Callable<T> task)");
          return super.submitListenable(task);
      }
  
  }
  ```

- 使用：

  ```java
  //ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
  ThreadPoolTaskExecutor executor = new VisiableThreadPoolTaskExecutor();
  ```



# JAVA 线程池

- Java通过Executors提供四种线程池，分别为：
  - newCachedThreadPool创建一个可缓存线程池，如果线程池长度超过处理需要，可灵活回收空闲线程，若无可回收，则新建线程。   
  - newFixedThreadPool 创建一个定长线程池，可控制线程最大并发数，超出的线程会在队列中等待。   
  - newScheduledThreadPool 创建一个定长线程池，支持定时及周期性任务执行。   
  - newSingleThreadExecutor 创建一个单线程化的线程池，它只会用唯一的工作线程来执行任务，保证所有任务按照指定顺序(FIFO, LIFO, 优先级)执行。   

-    优点  

  - ​    重用存在的线程，减少对象创建、消亡的开销，性能佳。   
  - ​    可有效控制最大并发线程数，提高系统资源的使用率，同时避免过多资源竞争，避免堵塞。   
  - ​    提供定时执行、定期执行、单线程、并发数控制等功能。   

- 代码实现

  - 配置类实现

    ```java
    @Configuration
    public class ThreadPoolConfig {
        
         /**
         * 获取虚拟机的最大可用的处理器数量
         * IO密集型任务  = 一般为2*CPU核心数（常出现于线程中：数据库数据交互、文件上传下载、网络数据传输等等）
         * CPU密集型任务 = 一般为CPU核心数+1（常出现于线程中：复杂算法）
         * 混合型任务  = 视机器配置和复杂度自测而定
         */
        private int corePoolSize = Runtime.getRuntime().availableProcessors();
        
        
        @Bean(name = "defaultThreadPool")
        public ThreadPoolTaskExecutor defaultThreadPool() {
            ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    
            //核心线程数目
            executor.setCorePoolSize(corePoolSize);
            // 指定最大线程数
            executor.setMaxPoolSize(corePoolSize*2);
            //队列中最大的数目
            executor.setQueueCapacity(1000);
            //线程名称前缀
            executor.setThreadNamePrefix("defaultThreadPool_");
            //rejection-policy：当pool已经达到max size的时候，如何处理新任务
            // CALLER_RUNS：不在新线程中执行任务，而是由调用者所在的线程来执行
            // 对拒绝task的处理策略
            executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
            //线程空闲后的最大存活时间
            executor.setKeepAliveSeconds(60);
            // 加载 executor.initialize();
            executor.initialize();
            return executor;
        }
    }
    ```

  - 方式一（CountDownLatch,线程同步）

    - CountDownLatch 是一个同步工具类，允许一个线程或者多个线程等待其他线程完成操作，再执行

    ```java
    /**
    * 线程池设计
    */
    @Service
    public class StatsDemoService {
    	// 记录日志
        private Logger logger = LoggerFactory.getLogger(StatsDemo.class);
    
        @Resource(name = "defaultThreadPool")
        private ThreadPoolTaskExecutor threadPoolTaskExecutor;
        
        
        public void runDemo(){
            try {
                logger.info("所有的统计任务开始与:{}", DateUtils.format(new Date(),"yyyy-MM-dd HH:mm:ss"));
                CountDownLatch latch = new CountDownLatch(5);
                threadPoolTaskExecutor.execute(new StatsRun("任务A", 1000, latch));
                threadPoolTaskExecutor.execute(new StatsRun("任务B", 1000, latch));
                threadPoolTaskExecutor.execute(new StatsRun("任务C", 1000, latch));
                threadPoolTaskExecutor.execute(new StatsRun("任务D", 1000, latch));
                threadPoolTaskExecutor.execute(new StatsRun("任务E", 1000, latch));
                latch.await();
                logger.info("所有的统计任务执行完成:{}", DateUtils.format(new Date(),"yyyy-MM-dd HH:mm:ss"));
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
    
    /**
    * 具体执行任务的工作类
    */
    public class StatsRun implements Runnable {
    
        private Logger logger = LoggerFactory.getLogger(StatsRun.class);
        private  String statsName;
        private int runTime;
        private CountDownLatch latch;
    
        public StatsRun( String statsName, int runTime, CountDownLatch latch) {
            this.statsName = statsName;
            this.runTime = runTime;
            this.latch = latch;
        }
    
        @Override
        public void run() {
            try {
                logger.info("{} 任务开始于 {}",statsName,DateUtils.format(new Date(),"yyyy-MM-dd HH:mm:ss"));
                System.out.println();
                //模拟任务执行时间
                Thread.sleep(runTime);
                logger.info("{} 任务完成于 {}",statsName, DateUtils.format(new Date(),"yyyy-MM-dd HH:mm:ss"));
                latch.countDown();//单次任务结束，计数器减一
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
    ```

  - 方式二（Future）

    ```java
    /**
    * 定义线程池
    */
    
    @Component
    public class StatsDemo1Service {
    
        private Logger logger = LoggerFactory.getLogger(StatsDemo1.class);
    
        @Resource(name = "defaultThreadPool")
        private ThreadPoolTaskExecutor executor;
        
        public void runDemo(){
                List<Future<String>> resultList = new ArrayList<Future<String>>();
                logger.info("所有的统计任务开始与:{}", DateUtils.format(new Date(),"yyyy-MM-dd HH:mm:ss"));
                // 使用submit提交异步任务，并且获取返回值为future
                resultList.add(executor.submit(new StatsRun1("任务A", 1000)));
                resultList.add(executor.submit(new StatsRun1("任务B", 1000)));
                resultList.add(executor.submit(new StatsRun1("任务C", 1000)));
                resultList.add(executor.submit(new StatsRun1("任务D", 1000)));
                resultList.add(executor.submit(new StatsRun1("任务E", 1000)));
    
                // 遍历任务结果
                for(Future<String> fs : resultList){
                    try {
                        //打印各个线任务执行的结果，调用future.get() 阻塞主线程，获取异步任务的返回结果
                        logger.info("StatsDemo1:{}",fs.get());
                    } catch (ExecutionException e) {
                        e.printStackTrace();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                logger.info("所有的统计任务执行完成:{}", DateUtils.format(new Date(),"yyyy-MM-dd HH:mm:ss"));
        }
    }
    
    /**
    * 线程要执行的任务
    */
    public class StatsRun1 implements Callable<String> {
        private Logger logger = LoggerFactory.getLogger(StatsRun1.class);
        private String statsName;
        private int runTime;
    
        public StatsRun1(String statsName, int runTime) {
            this.statsName = statsName;
            this.runTime = runTime;
        }
    
        @Override
        public String call() throws Exception {
            try {
                logger.info("{} 任务开始于 {}",statsName, DateUtils.format(new Date(),"yyyy-MM-dd HH:mm:ss"));
                //模拟任务执行时间
                Thread.sleep(runTime);
                logger.info("{} 任务完成于 {}",statsName,DateUtils.format(new Date(),"yyyy-MM-dd HH:mm:ss"));
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return "over";
        }
    }
    ```

  - 方式三

    - 重点是和springboot整合，采用注解bean方式生成ThreadPoolTaskExecutor
    - @Bean

    ```java
    //spring依赖包 import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor; @Configuration public class GlobalConfig { /**
         * 默认线程池线程池
         *
         * @return Executor
         */ @Bean public ThreadPoolTaskExecutor defaultThreadPool() { ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor(); //核心线程数目 executor.setCorePoolSize(16); //指定最大线程数 executor.setMaxPoolSize(64); //队列中最大的数目 executor.setQueueCapacity(16); //线程名称前缀 executor.setThreadNamePrefix("defaultThreadPool_"); //rejection-policy：当pool已经达到max size的时候，如何处理新任务 //CALLER_RUNS：不在新线程中执行任务，而是由调用者所在的线程来执行 //对拒绝task的处理策略 executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy()); //线程空闲后的最大存活时间 executor.setKeepAliveSeconds(60); //加载 executor.initialize(); return executor; }
    ```
    - 使用

      ```java
      //通过注解引入配置
      @Resource(name = "defaultThreadPool")
      private ThreadPoolTaskExecutor executor;
      ```

      ```java
      //使用Future方式执行多任务 //生成一个集合 List<Future> futures = new ArrayList<>(); //获取后台全部有效运营人员的集合 List<AdminUserMsgResponse> adminUserDOList = adminManagerService.GetUserToSentMsg(null); for (AdminUserMsgResponse response : adminUserDOList) { //并发处理 if (response.getMobile() != null) { Future<?> future = executor.submit(() -> {
                                          //发送短信
                                          mobileMessageFacade.sendCustomerMessage(response.getMobile(), msgConfigById.getContent());
                                      });
                                      futures.add(future);
                                  }
                              }
      
                            //查询任务执行的结果
                             for (Future<?> future : futureList) {
                                  while (true) {//CPU高速轮询：每个future都并发轮循，判断完成状态然后获取结果，这一行，是本实现方案的精髓所在。即有10个future在高速轮询，完成一个future的获取结果，就关闭一个轮询
                           if (future.isDone()&& !future.isCancelled()) {//获取future成功完成状态，如果想要限制每个任务的超时时间，取消本行的状态判断+future.get(1000*1, TimeUnit.MILLISECONDS)+catch超时异常使用即可。
                               Integer i = future.get();//获取结果
                              System.out.println("任务i="+i+"获取完成!"+new Date());
                              list.add(i);
                              break;//当前future获取结果完毕，跳出while
                          } else {
                              Thread.sleep(1);//每次轮询休息1毫秒（CPU纳秒级），避免CPU高速轮循耗空CPU---》新手别忘记这个
                          }
                      }
                   }
      ```


# springboot 切面 AOP 详解

### 切面方法说明

- @Aspect	: 作用把当前类标识为一个切面供容器读取
- @Before:  前置增强，相当于BeforeAdvice的功能
- @AfterReturning: 后置增强，相当于AfterReturningAdvice, 方法退出时执行
- @AfterThrowing: 异常抛出增强，相当于ThrowsAdvice
- @After： final增强，不管是抛出异常或者正常退出都会执行
- @Around：环绕增强，相当于MethodIntterceptor
- 说明：
  - 除了@Around外，其余方法的JoinPoint参数是可选的；JoinPoint里包含了类名、被切面的方法名，参数等属性。
  - @Around参数必须为ProceedingJoinPoint,pjp.proceed相应于执行被切面的方法.
  - @AfterReturning方法中，可选参数returning=“XXX”,"XXX"即为在controller里方法的返回值；
  - @AfterThrowing方法中，可以加throwing="XXX",供读取异常信息

### 切入点PointCut

- 切点函数execution
  - 用于匹配方法执行的连接点
  - 语法：execution(方法修饰符(可选)  返回类型  方法名  参数  异常模式(可选))
    - 参数部分允许使用通配符：
      - `*` 匹配任意字符，但只能匹配一个元素
      - `..` 匹配任意字符，可以匹配任意多个元素，表示类时，必须和`*`联合
      - `+` 必须跟在类名后面，如Dog+，表示类本身和继承或扩展指定类的所有类
- @ annotation()
  - 标注指定注解的目标类方法
    - 例如：` @annotation(org.springframework.transaction.annotation.Transactional) `表示标注了@Transactional的方法
- args()
  - 通过目标类方法的参数类型指定切点
    - 例如：`args(string)`表示有且仅有一个String型参数的方法
- @args()
  - 通过目标类参数的对象类型是否标注了指定注解指定切点
    - 例如：`@args(org.springframework.stereotype.Service)` 表示有且仅有一个标注了@Service的类参数的方法
- within()
  - 通过类名指定切点
    - 例如： `within(examples.chap03.Horseman)` 表示Horseman的所有方法
- target()
  - 通过类名指定，同时包含所有子类
    - 例如：`target(examples.chap03.Horseman)`  且Elephantman extends Horseman，则两个类的所有方法都匹配
- @within()
  - 匹配标注了指定注解的类及其所有子类
    - 例如：`@within(org.springframework.stereotype.Service)` 给Horseman加上@Service标注，则Horseman和Elephantman 的所有方法都匹配
- @target()
  - 所有标注了指定注解的类
    - 例如：`@target(org.springframework.stereotype.Service)` 表示所有标注了@Service的类的所有方法
- this()
  - 大部分时候和target()相同，区别是this是在运行时生成代理类后，才判断代理类与指定的对象类型是否匹配

### 逻辑运算符

- 表达式可由多个切点函数通过逻辑运算组成
- &&
  - 与操作，求交集，也可以写成 and
    - 例如： `execution(* chop(..)) && target(Horseman)`  表示Horseman及其子类的chop方法
- ||
  - 或操作，求并集，也可以写成or
    - 例如：` execution(* chop(..)) || args(String) ` 表示名称为chop的方法或者有一个String型参数的方法
- !
  - 非操作，求反集，也可以写成not
    - 例如：`例如 execution(* chop(..)) and !args(String)`  表示名称为chop的方法但是不能是只有一个String型参数的方法

### ElementType各枚举常量的含义

| 常量            | 含义                                                 |
| --------------- | ---------------------------------------------------- |
| ANNOTATION_TYPE | 注解类型声明                                         |
| CONSTRUCTOR     | 构造方法声明                                         |
| FIELD           | 属性、字段声明（包括枚举常量）                       |
| LOCAL_VARIABLE  | 局部变量声明                                         |
| METHOD          | 方法声明                                             |
| PACKAGE         | 包声明                                               |
| PARAMETER       | 参数声明                                             |
| TYPE            | 类、接口（包括注解类型）、枚举类型、用户自定义的注解 |
| TYPE_PARAMETER  | @since1.8                                            |
| TYPE_USE        | @since1.8                                            |

### @Retention注解 及RetentionPolicy 枚举常量

- @Retention 注解

  - 定义被它所注解的注解保留多久

- RetentionPolicy 枚举常量

  - SOURCE ：被编译器忽略
  - CLASS ：注解将会被保留在Class文件中，但在运行时并不会被VM保留。这是默认行为，所有没有用Retention注解的注解，都会采用这种策略
  - RUNTIME ：保留至运行时。所以我们可以通过反射去获取注解信息。

### 实例：

- 引入依赖

  ```xml
  <dependency>
     <groupId>org.springframework.boot</groupId>
     <artifactId>spring-boot-starter-aop</artifactId>
  </dependency>
  ```

- 创建实体类

  ```java
  public class SysLog implements Serializable {
      private Long id;
  
      private String username; //用户名
  
      private String operation; //操作
  
      private String method; //方法名
  
      private String params; //参数
  
      private String ip; //ip地址
  
      private Date createDate; //操作时间
      //创建getter和setter方法
  }
  ```

- 创建一个自定义注解类

  ```java
  /**
   * 自定义注解类
   */
  @Target(ElementType.METHOD) //注解放置的目标位置,METHOD是可注解在方法级别上
  @Retention(RetentionPolicy.RUNTIME) //注解在哪个阶段执行
  @Documented //生成文档
  public @interface MyLog {
      String value() default "";
  }
  ```

- 创建aop切面实现类

  ```java
  import com.alibaba.fastjson.JSON;
  import com.qfedu.rongzaiboot.annotation.MyLog;
  import com.qfedu.rongzaiboot.entity.SysLog;
  import com.qfedu.rongzaiboot.service.SysLogService;
  import com.qfedu.rongzaiboot.utils.HttpContextUtils;
  import com.qfedu.rongzaiboot.utils.IPUtils;
  import com.qfedu.rongzaiboot.utils.ShiroUtils;
  import org.aspectj.lang.JoinPoint;
  import org.aspectj.lang.annotation.AfterReturning;
  import org.aspectj.lang.annotation.Aspect;
  import org.aspectj.lang.annotation.Pointcut;
  import org.aspectj.lang.reflect.MethodSignature;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.stereotype.Component;
  
  import javax.servlet.http.HttpServletRequest;
  import java.lang.reflect.Method;
  import java.util.Date;
  
  /**
   * 系统日志：切面处理类
   */
  @Aspect
  @Component
  public class SysLogAspect {
  
      @Autowired
      private SysLogService sysLogService;
  
      //定义切点 @Pointcut
      //在注解的位置切入代码
      @Pointcut("@annotation( com.qfedu.rongzaiboot.annotation.MyLog)")
      public void logPoinCut() {
      }
  
      //切面 配置通知
      @AfterReturning("logPoinCut()")
      public void saveSysLog(JoinPoint joinPoint) {
          System.out.println("切面。。。。。");
          //保存日志
          SysLog sysLog = new SysLog();
  
          //从切面织入点处通过反射机制获取织入点处的方法
          MethodSignature signature = (MethodSignature) joinPoint.getSignature();
          //获取切入点所在的方法
          Method method = signature.getMethod();
  
          //获取操作
          MyLog myLog = method.getAnnotation(MyLog.class);
          if (myLog != null) {
              String value = myLog.value();
              sysLog.setOperation(value);//保存获取的操作
          }
  
          //获取请求的类名
          String className = joinPoint.getTarget().getClass().getName();
          //获取请求的方法名
          String methodName = method.getName();
          sysLog.setMethod(className + "." + methodName);
  
          //请求的参数
          Object[] args = joinPoint.getArgs();
          //将参数所在的数组转换成json
          String params = JSON.toJSONString(args);
          sysLog.setParams(params);
  
          sysLog.setCreateDate(new Date());
          //获取用户名
          sysLog.setUsername(ShiroUtils.getUserEntity().getUsername());
          //获取用户ip地址
          HttpServletRequest request = HttpContextUtils.getHttpServletRequest();
          sysLog.setIp(IPUtils.getIpAddr(request));
  
          //调用service保存SysLog实体类到数据库
          sysLogService.save(sysLog);
      }
  
  }
  ```

- 使用

  ```java
  //例如在contoller类的方法上加注解
  @RestController
  @RequestMapping("/sys/menu")
  public class SysMenuController extends AbstractController {
  
      @Autowired
      private SysMenuService sysMenuService;
  
      @MyLog(value = "删除菜单记录")  //这里添加了AOP的自定义注解
      @PostMapping("/del")
      public R deleteBatch(@RequestBody Long[] menuIds) {
          for (Long menuId : menuIds) {
              if (menuId <= 31) {
                  return R.error("系统菜单，不能删除");
              }
          }
          sysMenuService.deleteBatch(menuIds);
  
          return R.ok("删除成功");
      }
  }
  ```

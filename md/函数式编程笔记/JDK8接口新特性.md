# JDK8 接口新特性

#### lambda 表达式

- 示例：

  ```java
  Runnable target2 = () -> System.out.println("ok");
  ```

- 写法

  ```java
  Interface1 i1 = (i) -> i * 2;
  
  // 常见写法
  Interface1 i2 = i -> i * 2;
  
  Interface1 i3 = (int i) -> i * 2;
  
  Interface1 i4 = (int i) -> {
      System.out.println("----");
      return i * 2;
  };
  ```

- 函数式接口 

  - 注解 @FunctionalInterface
  - 要实现的方法只能有一个

- 默认方法（默认实现方法）

  - 在接口里面有默认的方法实现

#### 函数接口

| 接口              | 输入参数 | 返回值类型 | 说明                         |
| ----------------- | -------- | ---------- | ---------------------------- |
| Predicate<T>      | T        | boolean    | 断言                         |
| Consumer<T>       | T        | /          | 消费一个数据                 |
| Function<T,R>     | T        | R          | 输入T输出R的函数             |
| Supplier<T>       | /        | T          | 提供一个数据                 |
| UnaryOperator<T>  | T        | T          | 一元函数（输出输入类型相同） |
| BiFunction<T,U,R> | (T,U)    | R          | 2个输入的函数                |
| BinaryOperator<T> | (T,T)    | T          | 二元函数（输出输入类型相同） |

- 函数引用

  ```java
  // 方法引用
  Consumer<String> consumer = System.out::println;
  consumer.accept("1234");
  
  // 静态方法引用,类名::方法名
  Consumer<Dog> consumer1 = Dog::bark;
  Dog dog = new Dog();
  consumer1.accept(dog);
  
  //非静态方法引用，实例::方法名
  // Function<Integer,Integer> function = dog::eat;
  //UnaryOperator<Integer> function = dog::eat;
  //System.out.println("剩下"+ function.apply(2)+"斤");
  IntUnaryOperator function = dog::eat;
  System.out.println("剩下"+ function.applyAsInt(2)+"斤");
  
  // JAVA默认把当前实例传入到非静态方法，参数名为：this，位置第一个
  // 使用类名引用非静态方法，类名::方法名(非静态)
  BiFunction<Dog,Integer, Integer> eatFunction = Dog::eat;
  System.out.println("剩下"+ eatFunction.apply(dog,2)+"斤");
  
  //构造函数方法引用(无参)
  Supplier<Dog> supplier = Dog::new;
  System.out.println("创建了新对象："+supplier.get());
  
  // 构造函数方法引用(带参)
  Function<String,Dog> function1 = Dog::new;
  System.out.println("创建了新对象："+function1.apply("旺财"));
  ```

#### lambda表达式  类型推断

- ```java
  // 变量类型定义
  IMath lambda = (x,y) -> x+y;
  
  //数组里
  IMath[] lambdas = {(x,y) -> x+y};
  
  //强转
  Object lamdba2 = (IMath)(x,y) -> x+y;
  
  //通过返回值类型
  IMath createLambda = creteLamdba();
  
  TypeDemo typeDemo = new TypeDemo();
  // 当存在二义性(重载)的时候，使用强转对应的接口解决
  typeDemo.test((IMath) (x,y) -> x+y);
  ```

####  lambda表达式  变量引用

- 变量是final的

#### 级联表达式和柯里化

- ```java
  // 实现了x+y的级联表达式
  // 柯里化： 把多个参数的函数转换为只有一个参数的函数
  // 柯里化目的： 函数标准化
  // 高阶函数： 就是返回函数的函数
  Function<Integer,Function<Integer,Integer>> fun = x ->y -> x+y;
  System.out.println(fun.apply(2).apply(3));
  
  Function<Integer,Function<Integer,Function<Integer,Integer>>> fun2 =x -> y -> z -> x+y+z;
  System.out.println(fun2.apply(2).apply(3).apply(4));
  
  int[] nums = {2,3,4};
  Function f = fun2;
  for (int i = 0; i < nums.length; i++){
      if(f instanceof  Function){
          Object obj = f.apply(nums[i]);
          if(obj instanceof Function){
              f = (Function) obj;
          }else {
              System.out.println("调用结束：结果为" + obj);
          }
      }
  }
  ```

#### Stream 流编程

- 概念

- 外部迭代和内部迭代

  ```java
  // 外部迭代
  int sum = 0;
  for(int i: nums){
      sum += i;
  }
  System.out.println("结果为："+sum);
  
  // 使用stream的内部迭代
  // map 就是中间操作(返回stream的操作）
  // sum就是终止操作
  int sum2 = IntStream.of(nums).sum();
  System.out.println("结果为：" + sum2);
  ```

- 中间操作/终止操作和惰性求值

  ```java
  // 惰性求值就是终止没有调用的情况下，中间操作不会执行
  IntStream.of(nums).map(StreamDemo::doubleNum);
  ```

- 创建

  |            | 相关方法                               |
  | ---------- | -------------------------------------- |
  | 集合       | Collection.stream/parallelStream       |
  | 数组       | Arrays.stream                          |
  | 数字Stream | IntStream/LongStream.range/rangeClosed |
  |            | Random.ints/longs/doubles              |
  | 自己创建   | Stream.generate/iterate                |

  ```java
  //从集合创建
  List<String> list = new ArrayList<>();
  list.stream();
  list.parallelStream();
  
  //从数组创建
  Arrays.stream(new int[]{2,3,4,5});
  
  //创建数字流
  IntStream.of(1,2,3);
  IntStream.range(1,10);
  
  //使用random创建一个无限流
  new Random().ints();
  //使用random创建一个有限流
  new Random().ints().limit(10);
  
  //自己生产流
  Random random = new Random();
  Stream.generate(() -> random.nextInt()).limit(20);
  ```

- 中间操作

  |            | 相关方法             |
  | ---------- | -------------------- |
  | 无状态操作 | map/mapToXxx         |
  |            | flatMap/flatMapToXxx |
  |            | filter               |
  |            | peek                 |
  |            | unordered            |
  | 有状态操作 | distinct             |
  |            | sorted               |
  |            | limit/skip           |

  ```java
  String str = "my name is 007";
  
  // 把每个单词的长度打印出来
  Stream.of(str.split(" "))
      .filter(s -> s.length() > 2)
      .map(s -> s.length())
      .forEach(System.out::println);
  
  // flatMap A->B属性（是个集合），最终得到所有的元素里面的所有B属性集合
  // intStream/longStream 并不是Stream的子类，所以要进行装箱 boxed
  Stream.of(str.split(" "))
      .flatMap(s -> s.chars().boxed())
      .forEach(i -> System.out.println((char)i.intValue()));
  
  // peek 用于debug是个中间操作，和forEach是终止操作
  Stream.of(str.split(" "))
      .peek(System.out::println)
      .forEach(System.out::println);
  
  //limit,主要用于无限流
  new Random()
      .ints()
      .filter(i -> i>100 && i < 1000)
      .limit(10)
      .forEach(System.out::println);
  ```

- 终止操作

  |            | 相关方法                    |
  | ---------- | --------------------------- |
  | 非短路操作 | forEach/forEachOrdered      |
  |            | collect/toArray             |
  |            | reduce                      |
  |            | min/max/count               |
  | 短路操作   | findFirst/findAny           |
  |            | allMatch/anyMatch/noneMatch |

  ```java
  String str = "my name is 007";
  
  // 使用并行流
  str.chars().parallel().forEach(i -> System.out.print((char)i));
  System.out.println();
  // 使用forEachOrdered保证顺序
  str.chars().parallel().forEachOrdered(i -> System.out.print((char)i));
  System.out.println();
  
  // 收集到List
  List<String> list = Stream.of(str.split(" ")).collect(Collectors.toList());
  System.out.println(list);
  
  // 使用reduce拼接字符串
  Optional<String> reduce = Stream.of(str.split(" ")).reduce((s1, s2) -> s1 + "|" + s2);
  System.out.println(reduce.orElse(""));
  
  // 带初始化值的reduce
  String reduce1 = Stream.of(str.split(" ")).reduce("",(s1,s2) -> s1 + "|" + s2);
  System.out.println(reduce1);
  
  // 计算所有单词总长度
  Integer len = Stream.of(str.split(" ")).map(s -> s.length()).reduce(0,(s1,s2) -> s1 + s2);
  System.out.println(len);
  
  // max使用
  Optional<String> max = Stream.of(str.split(" ")).max((s1, s2) -> s1.length() - s2.length());
  System.out.println(max);
  
  // 使用 findFirst 实现短路操作
  OptionalInt first = new Random().ints().findFirst();
  System.out.println(first.getAsInt());
  ```

- 并行流

  ```java
  // 调用parallel产生一个并行流
  // 并行线程池使用的线程池：ForkJoinPool.commonPool
  // 默认的线程数是当前机器cpu的线程数
  // 使用 System.setProperty("java.util.concurrent.ForkJoinPool.common.parallelism","8") 设置默认线程数
  IntStream.range(1,100).parallel().peek(StreamDemo5::debug).count();
  
  // 实现这样一个效果，先并行，再串行
  // 多次调用 parallel/sequential，以最后一次调用为准
  IntStream.range(1,100)
              // 调用 parallel 产生一个并行
              .parallel().peek(StreamDemo5::debug)
              // 调用sequential 产生串行
              .sequential().peek(StreamDemo5::debug1)
              .count();
  
  //使用自己的线程池，不使用默认线程池，防止任务阻塞
  //  ForkJoinPool-1
  ForkJoinPool forkJoinPool = new ForkJoinPool();
  forkJoinPool.submit(() -> IntStream.range(1,100).parallel().peek(StreamDemo5::debug).count());
  forkJoinPool.shutdown();
  
  synchronized(forkJoinPool){
      try {
          forkJoinPool.wait();
      } catch (InterruptedException e) {
          e.printStackTrace();
      }
  }
  ```

- 收集器

  ```java
  // 测试数据
  List<Student> students = Arrays.asList(
      new Student("小明",10,Gender.MALE,Grade.ONE),
      new Student("大明",9,Gender.MALE,Grade.THREE),
      new Student("小白",8,Gender.FEMALE,Grade.TWO),
      new Student("小黑",13,Gender.FEMALE,Grade.FOUR),
      new Student("小红",7,Gender.FEMALE,Grade.THREE),
      new Student("小黄",13,Gender.MALE,Grade.ONE),
      new Student("小青",13,Gender.FEMALE,Grade.THREE),
      new Student("小紫",9,Gender.FEMALE,Grade.TWO),
      new Student("小王",6,Gender.MALE,Grade.ONE),
      new Student("小李",6,Gender.MALE,Grade.ONE),
      new Student("小马",14,Gender.FEMALE,Grade.FOUR),
      new Student("小刘",13,Gender.MALE,Grade.FOUR)
  );
  
  // 得到所有学生的年龄列表
  // s -> s.getAge() --> Student::getAge,不会多生成一个类似lambda$0
  List<Integer> ages = students.stream().map(Student::getAge).collect(Collectors.toList());
  System.out.println("所有学生年龄："+ages);
  
  // 统计汇总信息
  IntSummaryStatistics agesSummaryStatistics = students.stream().collect(Collectors.summarizingInt(Student::getAge));
  System.out.println("年龄汇总信息："+agesSummaryStatistics);
  
  // 分块
  Map<Boolean, List<Student>> genders = students.stream().collect(Collectors.partitioningBy(s -> s.getGender() == Gender.MALE));
  System.out.println("男女学生列表："+genders);
  
  // 分组
  Map<Grade, List<Student>> grades = students.stream().collect(Collectors.groupingBy(Student::getGrade));
  System.out.println("学生班级："+grades);
  
  //得到所有班级学生的个数
  Map<Grade, Long> gradesCount = students.stream().collect(Collectors.groupingBy(Student::getGrade,Collectors.counting()));
  System.out.println("每个班级学生个数列表："+gradesCount);
  ```

- 运行机制

  - 所有操作是链式调用，一个元素只迭代一次
  - 每一个中间操作返回一个新的流，流里面有一个属性sourceStage指向同一个地方，就是Head
  - Head -> nextStage -> nextStage->...->null
  - 有状态操作会把无状态操作截断，单独处理
  - 并行环境下，有状态的中间操作不一定能并行操作
  - parallel/sequetial 这两个操作也是中间操作（也是返回stream），但是它们不创建流，只修改Head的并行标志

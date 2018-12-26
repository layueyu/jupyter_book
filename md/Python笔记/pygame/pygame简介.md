# pygame 模块
- 官网： [https://www.pygame.org](https://www.pygame.org)
- 安装： `pip3 install pygame`
- 验证安装： `python3 -m pygame.examples.aliens`

# 初始化和退出
- pygame.init() 导入并初始化所有的pygame模块，使用其他模块之前必须调用init方法
- pygame.quit() 卸载所有pygame模块，在游戏结束之前调用

# 坐标系
- 原点： 在左上角（0，0）
- x轴： 水平方向向右，逐渐增加
- y轴： 垂直方向向下，逐渐增加

- 在游戏中，所有可见的元素都是以矩形区域来描述位置
    - 矩形区域四个要素:(x,y)(width,height)
    - pygame专门提供了一个类，pygame.Rect用于描述矩形区域
        - `Rect(x,y,width,height)`
        - 提示
            - pygame.Rect 是一个特殊类，内部只是封装一些数字计算
            - 不执行pygame.init() 方法能够直接使用

# 创建游戏主窗口
- pygame 提供一个模块 pygame.display用于创建、管理 游戏窗口
- 方法：
    - pygame.display.set_mode() 初始化游戏显示窗口
        - set_mode(resolution=(0,0), flags=0, depth=0)
        - 参数:
            - resolution: 指定屏幕的宽和高，默认创建窗口大小和屏幕大小一致
            - flags： 指定屏幕附加选项，默认不需要传递
            - depth：参数表示颜色位数，默认自动匹配
            - 返回值：
                游戏屏幕对象
    - pygame.display.update() 刷新屏幕内内容显示
        - 

# 图像文件处理
- 加载图像文件： pygame.image.load()
- 使用 游戏屏幕对象，调用 blit 方法将图像绘制到指定位置
    - blit(图像，位置)
- 使用 pygame.display.update() 刷新屏幕内内容显示

# 游戏循环
- 保证游戏不会直接退出
- 变化图像位置
    - 每隔 1/60秒移动一下图像位置
    - 调用 pygame.display.update() 刷新屏幕内内容显示
- 检测用户交互

# 游戏时钟
- pygame 专门提供一个类 pygame.time.Clock 可以非常方便的设置屏幕绘制速度
- 使用步骤
    - 在游戏初始化 创建 时钟对象
    - 在 游戏循环 中 让时钟对象调用 tick(帧率)方法
- tick 根据上次被调用时间，自动设置 游戏循环 中延时

# 监听事件
- pygame 通过 pygame.event.get() 获取用户当前做动作 的事件列表

# 精灵和精灵组
- pygame.sprite.Sprite 
    - 需派生子类
    - 存储 图像数据image 
    - 记录 位置 rect 的对象
    - update 更新精灵位置
    - kill() 从所有组中删除
- pygame.sprite.Group
     - add 向组内添加精灵
     - sprites 返回所有精灵列表
     - update 让组内的所有精灵调用update方法
     - draw(Surface) 将组内所有精灵image，绘制到Surface指定的rect位置


# 定时器
- pygame.time.set_timer() 
    - set_timer(eventid,milliseconds)
        - 创建一个事件
        - 在 游戏循环 的 事件监听 方法中捕获该事件
        - 第一个参数 事件代号 基于常量 pygame.USEREVENT 来指定
            - USEREVENT 是一个整数，在增加的事件可以使用 USEREVENT +1 指定
        - 第二个参数 事件触发 间隔的毫秒值

# 随机数
- random 模块

# 键盘模块
- pygame.key.get_pressed() 

# 碰撞检测
- pygame.sprite.groupcollide()
    - groupcollide(group1,group2,dokill2,dokill2,colloded=None)
        - dokill 设置为True，则发生碰撞的精灵将被自动移除
- pygame.sprite.spritecollide()
    - spritecollide(sprite. group, dokill, colloded= None) 



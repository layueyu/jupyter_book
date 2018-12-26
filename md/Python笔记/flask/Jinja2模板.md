# Jinja2 模板

#### 基本流程

- 模板

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Template</title>
  </head>
  <body>
      <h1>hello {{ name }}</h1>
  </body>
  </html>
  ```

- 渲染

  ```python
  @app.route("/")
  def index():
      # 使用 render_template 渲染模板
      return render_template("index.html", name="python")
  
  def index1():
      data = {
          'name': 'python'
      }
      #使用字典
      return render_template("index.html", **data)
  ```

#### 变量

- 类型

  ```html
  <p>{{mydict['key']}}</p>
  
  <p>{{mydict.key}}</p>
  
  <p>{{mylist[1]}}</p>
  
  <p>{{mylist[myvariable]}}</p>
  ```

- 渲染

  ```python
  from flask import Flask,render_template
  app = Flask(__name__)
  
  @app.route('/')
  def index():
      mydict = {'key':'silence is gold'}
      mylist = ['Speech', 'is','silver']
      myintvar = 0
  
      return render_template('vars.html',
                             mydict=mydict,
                             mylist=mylist,
                             myintvar=myintvar
                             )
  if __name__ == '__main__':
      app.run(debug=True)
  ```

#### 过滤器

- 字符串过滤器

  - safe：禁用转义

    ```html
    <p>{{ '<em>hello</em>' | safe }}</p>
    ```

  - capitalize：把变量值的首字母转成大写，其余字母转小写

    ```html
    <p>{{ 'hello' | capitalize }}</p>
    ```

  - lower：把值转成小写

    ```html
    <p>{{ 'HELLO' | lower }}</p>
    ```

  - upper：把值转成大写

    ```html
    <p>{{ 'hello' | upper }}</p>
    ```

  - title：把值中的每个单词的首字母都转成大写

    ```html
    <p>{{ 'hello' | title }}</p>
    ```

  - trim：把值的首尾空格去掉

    ```html
    <p>{{ ' hello world ' | trim }}</p>
    ```

  - reverse:字符串反转

    ```html
    <p>{{ 'olleh' | reverse }}</p>
    ```

  - format:格式化输出

    ```html\
     <p>{{ '%s is %d' | format('name',17) }}</p>
    ```

  - striptags：渲染之前把值中所有的HTML标签都删掉

    ```html
    <p>{{ '<em>hello</em>' | striptags }}</p>
    ```

- 支持链式使用过滤器

  ```html
  <p>{{ “ hello world  “ | trim | upper }}</p>
  ```

- 列表过滤器

  - first：取第一个元素

    ```html
    <p>{{ [1,2,3,4,5,6] | first }}</p>
    ```

  - last：取最后一个元素

    ```html
    <p>{{ [1,2,3,4,5,6] | last }}</p>
    ```

  - length：获取列表长度

    ```html
    <p>{{ [1,2,3,4,5,6] | length }}</p>
    ```

  - sum：列表求和

    ```html
    <p>{{ [1,2,3,4,5,6] | sum }}</p>
    ```

  - sort：列表排序

    ```html
    <p>{{ [6,2,3,1,5,4] | sort }}</p>
    ```

- 自定义过滤器

  - 方式一

    ```python
    # add_template_filter (过滤器函数, 模板中使用的过滤器名字)
    def filter_double_sort(ls):
        return ls[::2]
    app.add_template_filter(filter_double_sort,'double_2')
    ```

  - 方式2

    ```python
    # 通过装饰器  app.template_filter (模板中使用的装饰器名字)
    @app.template_filter('db3')
    def filter_double_sort(ls):
        return ls[::-3]
    ```

#### 表单

- 安装

  ```shell
  pip install Flask-WTF
  ```

- WTForms支持的HTML标准字段

  | 字段对象            | 说明                                |
  | ------------------- | ----------------------------------- |
  | StringField         | 文本字段                            |
  | TextAreaField       | 多行文本字段                        |
  | PasswordField       | 密码文本字段                        |
  | HiddenField         | 隐藏文本字段                        |
  | DateField           | 文本字段，值为datetime.date格式     |
  | DateTimeField       | 文本字段，值为datetime.datetime格式 |
  | IntegerField        | 文本字段，值为整数                  |
  | DecimalField        | 文本字段，值为decimal.Decimal       |
  | FloatField          | 文本字段，值为浮点数                |
  | BooleanField        | 复选框，值为True和False             |
  | RadioField          | 一组单选框                          |
  | SelectField         | 下拉列表                            |
  | SelectMultipleField | 下拉列表，可选择多个值              |
  | FileField           | 文本上传字段                        |
  | SubmitField         | 表单提交按钮                        |
  | FormField           | 把表单作为字段嵌入另一个表单        |
  | FieldList           | 一组指定类型的字段                  |

- WTForms常用验证函数

  | 验证函数     | 说明                                     |
  | ------------ | ---------------------------------------- |
  | DataRequired | 确保字段中有数据                         |
  | EqualTo      | 比较两个字段的值，常用于比较两次密码输入 |
  | Length       | 验证输入的字符串长度                     |
  | NumberRange  | 验证输入的值在数字范围内                 |
  | URL          | 验证URL                                  |
  | AnyOf        | 验证输入值在可选列表中                   |
  | NoneOf       | 验证输入值不在可选列表中                 |

- 不使用 Flask-WTF 扩展时，表单需要自己处理

  ```html
  #模板文件
  <form method='post'>
      <input type="text" name="username" placeholder='Username'>
      <input type="password" name="password" placeholder='password'>
      <input type="submit">
  </form>
  ```

  ```python
  from flask import Flask,render_template,request
  
  @app.route('/login',methods=['GET','POST'])
  def login():
      if request.method == 'POST':
          username = request.form['username']
          password = request.form['password']
          print username,password
      	return “success”
  	else:
  		return render_template(“login.html”)
  ```

- 使用 Flask-WTF 扩展

  - 要设置 SECRET_KEY 的配置参数

  - 模板页

    ```html
    <form method="post">
            #设置csrf_token
            {{ form.csrf_token() }}
            {{ form.us.label }}
            <p>{{ form.us }}</p>
            {{ form.ps.label }}
            <p>{{ form.ps }}</p>
            {{ form.ps2.label }}
            <p>{{ form.ps2 }}</p>
            <p>{{ form.submit() }}</p>
            {% for x in get_flashed_messages() %}
                {{ x }}
            {% endfor %}
     </form>
    ```

  - 试图函数

    ```python
    from flask import Flask,render_template, redirect,url_for,session,request,flash
    
    #导入wtf扩展的表单类
    from flask_wtf import FlaskForm
    #导入自定义表单需要的字段
    from wtforms import SubmitField,StringField,PasswordField
    #导入wtf扩展提供的表单验证器
    from wtforms.validators import DataRequired,EqualTo
    app = Flask(__name__)
    app.config['SECRET_KEY']='1'
    
    #自定义表单类，文本字段、密码字段、提交按钮
    class Login(Flask Form):
        us = StringField(label=u'用户：',validators=[DataRequired()])
        ps = PasswordField(label=u'密码',validators=[DataRequired(),EqualTo('ps2','err')])
        ps2 = PasswordField(label=u'确认密码',validators=[DataRequired()])
        submit = SubmitField(u'提交')
    
    #定义根路由视图函数，生成表单对象，获取表单数据，进行表单数据验证
    @app.route('/',methods=['GET','POST'])
    def index():
        form = Login()
        if form.validate_on_submit():
            name = form.us.data
            pswd = form.ps.data
            pswd2 = form.ps2.data
            print name,pswd,pswd2
            return redirect(url_for('login'))
        else:
            if request.method=='POST':
    flash(u'信息有误，请重新输入！')
    
        return render_template('index.html',form=form)
    if __name__ == '__main__':
        app.run(debug=True)
    ```

#### 控制语句

- if语句

  ```html
  {% if %} 
  {% endif %}
  ```

- for语句

  ```html
  {% for item in samples %} 
  
  {% endfor %}
  ```

#### 宏

- 不带参数宏

  - 定义：

    ```html
    {% macro input() %}
    
      <input type="text"
    
             name="username"
    
             value=""
    
             size="30"/>
    
    {% endmacro %}
    ```

  - 使用

    ```html
    {{ input() }}
    ```

- 带参数宏

  - 定义：

    ```html
    {% macro input(name,value='',type='text',size=20) %}
        <input type="{{ type }}"
               name="{{ name }}"
               value="{{ value }}"
               size="{{ size }}"/>
    {% endmacro %}
    ```

  - 使用

    ```html
    {{ input(value='name',type='password',size=40)}}
    ```

- 将宏单独封装在html文件中

  - 文件名可以自定义macro.html

    ```html
    {% macro input() %}
    
        <input type="text" name="username" placeholde="Username">
        <input type="password" name="password" placeholde="Password">
        <input type="submit">
    {% endmacro %}
    ```

  - 在其它模板文件中先导入，再调用

    ```html
    {% import 'macro.html' as func %}
    {% func.input() %}
    ```

#### 模板继承

- 父模板：base.html

  ```html
   {% block top %}
      顶部菜单
    {% endblock top %}
  
    {% block content %}
    {% endblock content %}
  
    {% block bottom %}
      底部
    {% endblock bottom %}
  ```

- 子模版：

  ```html
  {% extends 'base.html' %}
  {% block content %}
  需要填充的内容
  {% endblock content %}
  ```

  - 模板继承使用时注意点：
    - 不支持多继承。
    - 为了便于阅读，在子模板中使用extends时，尽量写在模板的第一行。
    - 不能在一个模板文件中定义多个相同名字的block标签。
    - 当在页面中使用多个block标签时，建议给结束标签起个名字，当多个block嵌套时，阅读性更好

#### 包含

- Jinja2模板中，除了宏和继承，还支持一种代码重用的功能，叫包含(Include)。它的功能是将另一个模板整个加载到当前模板中，并直接渲染。

- 示例：
  - include的使用

    ```html
    {\% include 'hello.html' %}
    ```

- 包含在使用时，如果包含的模板文件不存在时，程序会抛出TemplateNotFound异常，可以加上ignore missing关键字。如果包含的模板文件不存在，会忽略这条include语句。

  示例：

  include的使用加上关键字ignore missing

  ```html
  {\% include 'hello.html' ignore missing %}
  ```

- 宏、继承、包含：

  - 宏(Macro)、继承(Block)、包含(include)均能实现代码的复用。
  - 继承(Block)的本质是代码替换，一般用来实现多个页面中重复不变的区域。
  - 宏(Macro)的功能类似函数，可以传入参数，需要定义、调用。
  - 包含(include)是直接将目标模板文件整个渲染出来。

####  Flask中的特殊变量和方法

-  在Flask中，有一些特殊的变量和方法是可以在模板文件中直接访问的。

-  config 对象:

  ```html
  config 对象就是Flask的config对象，也就是 app.config 对象。
  
  {{ config.SQLALCHEMY_DATABASE_URI }}
  ```

- request 对象:
  - 就是 Flask 中表示当前请求的 request 对象，request对象中保存了一次HTTP请求的一切信息。

  - request常用的属性如下：

    | 属性    | 说明                           | 类型           |
    | ------- | ------------------------------ | -------------- |
    | data    | 记录请求的数据，并转换为字符串 | *              |
    | form    | 记录请求中的表单数据           | MultiDict      |
    | args    | 记录请求中的查询参数           | MultiDict      |
    | cookies | 记录请求中的cookie信息         | Dict           |
    | headers | 记录请求中的报文头             | EnvironHeaders |
    | method  | 记录请求使用的HTTP方法         | GET/POST       |
    | url     | 记录请求的URL地址              | string         |
    | files   | 记录请求上传的文件             | *              |

    ```html
    {{ request.url }}
    ```

- url_for 方法:
  - url_for() 会返回传入的路由函数对应的URL，所谓路由函数就是被 app.route() 路由装饰器装饰的函数。如果我们定义的路由函数是带有参数的，则可以将这些参数作为命名参数传入。

  - ```html
    {{ url_for('index') }}
    
    {{ url_for('post', post_id=1024) }}
    ```

- get_flashed_messages方法：
  - 返回之前在Flask中通过 flash() 传入的信息列表。把字符串对象表示的消息加入到一个消息队列中，然后通过调用 get_flashed_messages() 方法取出。

  - ```html
    {% for message in get_flashed_messages() %}
        {{ message }}
    {% endfor %}
    ```


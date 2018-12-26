# abort函数与自定义异常处理

#### abort函数

- ```python
  from flask import abort
  ```

- 使用

  ```python
  // 传递状态码，必须是标准的http状态码
  abort(403)
  
  // 传递响应体信息
  resp = Response('err msg')
  abort(resp)
  ```

#### 自定义异常

- ```python
  @app.errhandle(404)
  def handle_404_error(err):
      ###这个函数返回前端用户看到的最终结果  ###
      return '出现404异常，{}'。format(err)
  ```



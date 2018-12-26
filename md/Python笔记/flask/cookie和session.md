# cookie 和 session

#### cookie

- 设置

  - ```python
    resp = make_response('success')
    resp.set_cookie('cast','python')
    # 设置过期时间
    resp.set_cookie('cast1','python1', max_age=3600)
    ```

- 获取

  - ```python
    request.cookies.get('cast')
    ```

- 删除

  - ```python
    resp = make_response('success')
    resp.delete_cookie('cast', 'python')
    ```

#### session

- ```python
  from flask import session
  ```

- 设置

  - ```python
    # flask 必须设置secret_key
    app.config['SECRET_KEY'] = 'asfasdgfsdg'
    session['key'] = 'value'
    ```

- 获取

  - ```python
    session.get('key')
    ```

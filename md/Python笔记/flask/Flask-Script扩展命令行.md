# Flask-Script扩展命令行

- 安装

  - ```shell
    pip install Flask-Script
    ```

- 使用

  - ```python
    from flask import Flask
    from flask_script import Manager
    
    app = Flask(__name__)
    
    manager = Manager(app)
    
    @app.route('/')
    def index():
        return '床前明月光'
    
    if __name__ == "__main__":
        manager.run() 
    ```

  - 


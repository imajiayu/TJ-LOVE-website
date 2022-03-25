import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import User

#创建flaskapp实例
app = create_app('default')

#创建数据库
@app.before_first_request
def create_db():
    db.create_all()

if __name__ == '__main__':
    app.run()

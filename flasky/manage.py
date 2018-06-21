#!/usr/bin/env python3
# coding=utf-8

from app import create_app, db
from app.models import Novel, Chapter
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Novel=Novel, Chapter=Chapter)


# 为shell命令注册一个make_context回调函数
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# 为了运行测试单元,添加了一个自定义的命令
@manager.command
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()

#!/usr/bin/env python3
# coding=utf-8

import logging
import re
from app import create_app, db
from app.models import Novel, Chapter
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app.novel.getter import get_novel, get_novel_info, get_novel_chapters, get_chapter_content
from app.novel.chinese_digit import getResultForDigit

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


@manager.command
def update_novel(name):
    """更新文章"""
    novel_url = get_novel(name)
    name, author = get_novel_info(novel_url)
    novel = Novel.query.filter_by(name=name).first()
    if not novel:
        logging.info('添加文章')
        novel = Novel(name=name, author=author)
        db.session.add(novel)
    print(novel.id)
    chapters = get_novel_chapters(novel_url)
    all_chapters = []
    for _ in chapters:
        title, chapter_url = _
        try:
            chapter = re.findall(r'\d{1,}', title)[0] if re.findall(r'\d{1,}', title) else getResultForDigit(title.split()[0].replace('第', '').replace('章', ''))
        except Exception as e:
            logging.info(e)
        else:
            all_chapters.append((name, chapter, title, chapter_url))
            logging.info(chapter, title, chapter_url)
            # novel = Novel.query.filter(Novel.name.contains(name)).first()
            # novel = Novel.query.filter(Novel.name==name).first()
            logging.warning(novel.id)
            new_chapter = Chapter.query.filter(Chapter.chapter==chapter, Chapter.novel_id==novel.id).first()
            logging.warning(new_chapter)
            # logging.info('chapter:', new_chapter)
            if not new_chapter:
                logging.warning('添加章节')
                content = get_chapter_content(chapter_url).strip()
                new_chapter = Chapter(title=title, chapter=chapter, content=content, novel_id=novel.id)
                db.session.add(new_chapter)


if __name__ == '__main__':
    print('Starting the API')
    manager.run()

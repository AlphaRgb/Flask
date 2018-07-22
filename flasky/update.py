import logging
import re

from app import db, create_app
from app.models import Novel, Chapter

from app.novel.getter import get_novel, get_novel_info, get_novel_chapters, get_chapter_content
from app.novel.chinese_digit import getResultForDigit


def update_novel(name):
    app = create_app('default')
    app_context = app.app_context()
    app_context.push()
    print(db.session)
    novel_url = get_novel(name)
    print(novel_url)
    name, author = get_novel_info(novel_url)
    print(name, author)
    novel = Novel(name='测试', author='测试')
    print(novel)
    novel = db.session().query(Novel).filter(Novel.name == '龙王传说').one()
    print(novel)
    # db.session.add(novel)
    # db.session.commit()
    # novel = Novel.query.filter_by(name=name).first()
    # if not novel:
    #     logging.info('添加文章')
    #     novel = Novel(name=name, author=author)
    #     db.session.add(novel)
    # print(novel.id)
    # chapters = get_novel_chapters(novel_url)
    # all_chapters = []
    # for _ in chapters:
    #     title, chapter_url = _
    #     try:
    #         chapter = re.findall(r'\d{1,}', title)[0] if re.findall(r'\d{1,}', title) else getResultForDigit(title.split()[0].replace('第', '').replace('章', ''))
    #     except Exception as e:
    #         logging.info(e)
    #     else:
    #         all_chapters.append((name, chapter, title, chapter_url))
    #         logging.info(chapter, title, chapter_url)
    #         # novel = Novel.query.filter(Novel.name.contains(name)).first()
    #         # novel = Novel.query.filter(Novel.name==name).first()
    #         logging.warning(novel.id)
    #         new_chapter = Chapter.query.filter(Chapter.chapter==chapter, Chapter.novel_id==novel.id).first()
    #         logging.warning(new_chapter)
    #         # logging.info('chapter:', new_chapter)
    #         if not new_chapter:
    #             logging.warning('添加章节')
    #             content = get_chapter_content(chapter_url).strip()
    #             new_chapter = Chapter(title=title, chapter=chapter, content=content, novel_id=novel.id)
    #             db.session.add(new_chapter)


if __name__ == '__main__':
    update_novel('龙王传说')
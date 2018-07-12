import re
import logging

from . import novel
from .. import db
from ..models import Novel, Chapter
from .getter import get_novel, get_novel_info, get_novel_chapters, get_chapter_content
from flask import jsonify
from .chinese_digit import getResultForDigit


@novel.route('/novel/<name>/')
def novel(name):
    novel_url = get_novel(name)
    name, author = get_novel_info(novel_url)
    novel = Novel.query.filter_by(name=name).first()
    if not novel:
        logging.info('添加文章')
        novel = Novel(name=name, author=author)
        db.session.add(novel)
    chapters = get_novel_chapters(novel_url)
    all_chapters = []
    for _ in chapters:
        all_chapters.append(_)
        title, chapter_url = _
        try:
            chapter = re.findall(r'\d{1,}', title)[0] if re.findall(r'\d{1,}', title) else getResultForDigit(title.split()[0].replace('第', '').replace('章', ''))
        except Exception as e:
            logging.info(e)
        else:
            logging.info(chapter, title, chapter_url)
            content = get_chapter_content(chapter_url).strip()
            logging.info(content)
            novel = Novel.query.filter(Novel.name.contains(name)).first()
            logging.info('novel:', novel.id, chapter)
            new_chapter = Chapter.query.filter(Chapter.chapter==chapter, Chapter.novel_id==novel.id).first()
            logging.info('chapter:', new_chapter)
            if not new_chapter:
                logging.info('添加章节')
                new_chapter = Chapter(title=title, chapter=chapter, content=content, novel_id=novel.id)
                logging.info('chapter:', new_chapter)
                db.session.add(new_chapter)
    results = {
        'title': name,
        'chapters': all_chapters
    }
    return jsonify(results)

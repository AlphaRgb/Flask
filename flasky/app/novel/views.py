import re
import logging

from . import novel
from .. import db

from ..models import Novel, Chapter
from .getter import get_novel, get_novel_info, get_novel_chapters, get_chapter_content
from flask import jsonify, render_template, redirect, url_for, request
from .chinese_digit import getResultForDigit
from .forms import SearchForm


@novel.route('/novels/<name>/')
def novel_index(name):
    """获取对应小说的最新章节"""
    novel = Novel.query.filter_by(name=name).first()
    if novel:
        chapters = Chapter.query.filter(Chapter.novel_id == novel.id).order_by(Chapter.chapter.desc()).all()
        all_chapters = []
        for chapter in chapters:
            title, chapter, content = chapter.title, chapter.chapter, chapter.content
            all_chapters.append((name, chapter, title))
    else:
        logging.info('添加小说')
        novel_url = get_novel(name)
        name, author = get_novel_info(novel_url)
        novel = Novel(name=name, author=author)
        db.session.add(novel)
        chapters = get_novel_chapters(novel_url)
        all_chapters = []
        for _ in chapters:
            title, chapter_url = _
            try:
                chapter = re.findall(r'\d{1,}', title)[0] if re.findall(r'\d{1,}', title) else getResultForDigit(title.split()[0].replace('第', '').replace('章', ''))
            except Exception as e:
                logging.info(e)
            else:
                all_chapters.append((name, chapter, title))
                logging.info(chapter, title, chapter_url)
                # novel = Novel.query.filter(Novel.name.contains(name)).first()
                # novel = Novel.query.filter(Novel.name==name).first()
                logging.info(novel.id)
                new_chapter = Chapter.query.filter(Chapter.chapter==chapter, Chapter.novel_id==novel.id).first()
                logging.info(new_chapter)
                # logging.info('chapter:', new_chapter)
                if not new_chapter:
                    logging.info('添加章节')
                    content = get_chapter_content(chapter_url).strip()
                    new_chapter = Chapter(title=title, chapter=chapter, content=content, novel_id=novel.id)
                    db.session.add(new_chapter)
    novel = {
        'title': name,
        'chapters': all_chapters
    }
    # return jsonify(novel)
    return render_template('novel.html', novel=novel)

@novel.route('/novels/', methods=['GET', 'POST'])
def novels():
    form = SearchForm()
    if form.validate_on_submit():
        data = form.search.data
        print('data:', data)
        return redirect(url_for('novel.novel_index', name=data))
    novels = Novel.query.all()
    return render_template('novels.html', novels=novels, form=form)


@novel.route('/novels/<novel_name>/<int:chapter_id>')
def novel(novel_name, chapter_id):
    novel = Novel.query.filter(Novel.name == novel_name).first()
    chapter = Chapter.query.filter(Chapter.novel_id==novel.id, Chapter.chapter==chapter_id).first()
    return render_template('content.html', chapter=chapter, name=novel_name)

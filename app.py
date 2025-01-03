from flask import Flask, render_template, abort, jsonify
from flask_flatpages import FlatPages, Page
from datetime import datetime
from collections import defaultdict
import os
import json
from datetime import datetime, date

# 配置
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'data/posts'
POST_DIR = 'posts'
FLATPAGES_ENCODING = 'utf-8'
FLATPAGES_MARKDOWN_EXTENSIONS = ['extra', 'codehilite']
FLATPAGES_YAML_DELIMITER = ''  # 不使用YAML分隔符

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.globals['now'] = datetime.now()
pages = FlatPages(app)

def parse_date(date_str):
    """解析日期字符串"""
    if isinstance(date_str, (datetime, date)):
        return date_str
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except (ValueError, TypeError):
        return datetime.now()

def get_posts():
    """获取所有文章，按日期排序"""
    return sorted(pages, key=lambda p: parse_date(p.meta.get('date')), reverse=True)

def get_categories():
    """获取所有分类及其文章数量"""
    categories = defaultdict(int)
    for page in pages:
        categories[page.meta.get('category', '未分类')] += 1
    return dict(categories)

def get_tags():
    """获取所有标签"""
    tags = set()
    for page in pages:
        tags.update(page.meta.get('tags', []))
    return sorted(tags)

def get_archive():
    """按年月归档文章"""
    archive = defaultdict(lambda: defaultdict(list))
    for page in pages:
        date = parse_date(page.meta.get('date'))
        archive[date.year][date.month].append(page)
    return dict(archive)

@app.route('/')
def index():
    """首页：显示最新文章列表"""
    posts = get_posts()
    return render_template('index.html', posts=posts)

@app.route('/post/<path:path>/')
def post(path):
    """文章详情页"""
    page = pages.get_or_404(path)
    return render_template('post.html', post=page)

@app.route('/category/<string:category>/')
def category(category):
    """分类页面"""
    posts = [p for p in pages if p.meta.get('category', '未分类') == category]
    if not posts:
        abort(404)
    return render_template('category.html', category=category, posts=posts)

@app.route('/tag/<string:tag>/')
def tag(tag):
    """标签页面"""
    posts = [p for p in pages if tag in p.meta.get('tags', [])]
    if not posts:
        abort(404)
    return render_template('tag.html', tag=tag, posts=posts)

@app.route('/archive/')
def archive():
    """归档页面"""
    archive_dict = get_archive()
    return render_template('archive.html', archive=archive_dict)

@app.route('/categories/')
def categories():
    """分类列表页面"""
    return render_template('categories.html', categories=get_categories())

@app.route('/tags/')
def tags():
    """标签列表页面"""
    return render_template('tags.html', tags=get_tags())

@app.template_filter('datetime')
def format_datetime(value, format='%Y-%m-%d'):
    """日期格式化过滤器"""
    if isinstance(value, str):
        return value
    return value.strftime(format)

@app.route('/search-data.json')
def search_data():
    """生成搜索数据"""
    posts_data = []
    for page in pages:
        posts_data.append({
            'title': page.meta.get('title', ''),
            'url': f'/post/{page.path}/',
            'date': format_datetime(page.meta.get('date', datetime.now())),
            'category': page.meta.get('category', '未分类'),
            'tags': page.meta.get('tags', []),
            'content': page.html[:200] + '...' if len(page.html) > 200 else page.html
        })
    return jsonify(posts_data)

if __name__ == '__main__':
    app.run(debug=True)

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

# 配置
DEBUG = False
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'data/posts'
FREEZER_DESTINATION = 'build'
FREEZER_RELATIVE_URLS = True
POST_DIR = 'posts'

# 初始化 Flask
app = Flask(__name__)
app.config.from_object(__name__)

# 初始化 FlatPages 和 Freezer
pages = FlatPages(app)
freezer = Freezer(app)

def get_posts():
    """获取所有文章，按日期排序"""
    return sorted(pages, key=lambda p: p.meta.get('date', datetime.now()), reverse=True)

def get_categories():
    """获取所有分类及其文章数量"""
    categories = {}
    for page in pages:
        category = page.meta.get('category', '未分类')
        categories[category] = categories.get(category, 0) + 1
    return categories

def get_tags():
    """获取所有标签"""
    tags = set()
    for page in pages:
        tags.update(page.meta.get('tags', []))
    return sorted(tags)

def get_archive():
    """按年月归档文章"""
    archive = {}
    for page in pages:
        date = page.meta.get('date', datetime.now())
        year = date.year
        month = date.month
        if year not in archive:
            archive[year] = {}
        if month not in archive[year]:
            archive[year][month] = []
        archive[year][month].append(page)
    return archive

@app.route('/')
def index():
    """首页"""
    return render_template('index.html', posts=get_posts())

@app.route('/post/<path:path>/')
def post(path):
    """文章页"""
    page = pages.get_or_404(path)
    return render_template('post.html', post=page)

@app.route('/category/<string:category>/')
def category(category):
    """分类页"""
    posts = [p for p in pages if p.meta.get('category', '未分类') == category]
    return render_template('category.html', category=category, posts=posts)

@app.route('/tag/<string:tag>/')
def tag(tag):
    """标签页"""
    posts = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', tag=tag, posts=posts)

@app.route('/archive/')
def archive():
    """归档页"""
    return render_template('archive.html', archive=get_archive())

@app.route('/categories/')
def categories():
    """分类列表页"""
    return render_template('categories.html', categories=get_categories())

@app.route('/tags/')
def tags():
    """标签列表页"""
    return render_template('tags.html', tags=get_tags())

@app.template_filter('datetime')
def format_datetime(value, format='%Y-%m-%d'):
    """日期格式化过滤器"""
    if isinstance(value, str):
        return value
    return value.strftime(format)

@freezer.register_generator
def page_generator():
    """生成所有页面的URL"""
    # 生成文章页面
    for page in pages:
        yield 'post', {'path': page.path}
    
    # 生成分类页面
    for category in get_categories().keys():
        yield 'category', {'category': category}
    
    # 生成标签页面
    for tag in get_tags():
        yield 'tag', {'tag': tag}

def copy_static_files():
    """复制静态文件到构建目录"""
    static_source = Path('static')
    static_dest = Path(FREEZER_DESTINATION) / 'static'
    
    if static_source.exists():
        if static_dest.exists():
            shutil.rmtree(static_dest)
        shutil.copytree(static_source, static_dest)

    # 复制图片
    images_source = Path('data/images')
    images_dest = Path(FREEZER_DESTINATION) / 'images'
    
    if images_source.exists():
        if images_dest.exists():
            shutil.rmtree(images_dest)
        shutil.copytree(images_source, images_dest)

def generate_search_data():
    """生成搜索数据文件"""
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
    
    search_data_path = os.path.join(FREEZER_DESTINATION, 'static', 'js')
    os.makedirs(search_data_path, exist_ok=True)
    
    with open(os.path.join(search_data_path, 'search-data.js'), 'w', encoding='utf-8') as f:
        f.write(f'window.posts = {json.dumps(posts_data, ensure_ascii=False, indent=2)};')

def main():
    """主函数"""
    # 确保构建目录存在
    os.makedirs(FREEZER_DESTINATION, exist_ok=True)
    
    # 生成静态文件
    freezer.freeze()
    
    # 复制静态文件
    copy_static_files()
    
    # 生成搜索数据
    generate_search_data()
    
    print(f'网站已生成到 {FREEZER_DESTINATION} 目录')

if __name__ == '__main__':
    main()

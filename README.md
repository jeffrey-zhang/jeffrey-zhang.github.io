# ZHANG.PRESS

一个基于Flask和GitHub Pages的个人博客系统。

## 功能特点

- 支持Markdown格式写作
- 文章分类和标签管理
- 按日期归档
- 全文搜索功能
- 响应式设计，支持移动端访问
- 评论系统（基于GitHub Issues）

## 目录结构

```
.
├── data/
│   ├── posts/      # Markdown文章
│   └── images/     # 文章图片
├── static/
│   └── js/         # JavaScript文件
├── templates/      # 模板文件
└── build/         # 构建输出目录
```

## 写作指南

1. 在`data/posts`目录下创建Markdown文件
2. 文件名格式：`YYYY-MM-DD-title.md`
3. 文件开头需要包含以下frontmatter:

```markdown
title: 文章标题
date: YYYY-MM-DD
category: 分类名
tags: [标签1, 标签2]
description: 文章描述
```

## 本地开发

1. 克隆仓库：
```bash
git clone https://github.com/jeffrey-zhang/jeffrey-zhang.github.io.git
cd jeffrey-zhang.github.io
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行开发服务器：
```bash
python app.py
```

4. 访问 http://localhost:5000

## 部署

项目使用GitHub Actions自动部署到GitHub Pages。每次推送到main分支时会自动触发构建和部署。

1. 确保仓库已启用GitHub Pages功能
2. 将代码推送到main分支
3. GitHub Actions会自动构建并部署网站

## 许可证

MIT License

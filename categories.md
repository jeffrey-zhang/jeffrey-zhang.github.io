---
layout: page
title: 分类
permalink: /categories/
---

{% for category in site.categories %}
  <h2 id="{{ category[0] }}">{{ category[0] }} ({{ category[1].size }})</h2>
  <ul>
    {% for post in category[1] %}
      <li>
        <span class="post-meta">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </li>
    {% endfor %}
  </ul>
{% endfor %}

{% if site.categories.size == 0 %}
  <p>暂无分类。</p>
{% endif %}

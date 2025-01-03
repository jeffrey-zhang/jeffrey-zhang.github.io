---
layout: page
title: 标签
permalink: /tags/
---

<div class="tag-cloud">
  {% assign tags = site.tags | sort %}
  {% for tag in tags %}
    <a href="#{{ tag[0] }}" style="font-size: {{ tag[1].size | times: 2 | plus: 12 }}px">
      {{ tag[0] }} ({{ tag[1].size }})
    </a>
  {% endfor %}
</div>

{% if site.tags.size == 0 %}
  <p>暂无标签。</p>
{% else %}
  <hr>

  {% for tag in site.tags %}
    <h2 id="{{ tag[0] }}">{{ tag[0] }}</h2>
    <ul>
      {% for post in tag[1] %}
        <li>
          <span class="post-meta">{{ post.date | date: "%Y-%m-%d" }}</span>
          <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        </li>
      {% endfor %}
    </ul>
  {% endfor %}
{% endif %}

<style>
.tag-cloud {
  margin-bottom: 2em;
  text-align: center;
  line-height: 2;
}
.tag-cloud a {
  margin: 0 0.5em;
  white-space: nowrap;
  text-decoration: none;
}
.tag-cloud a:hover {
  text-decoration: underline;
}
</style>

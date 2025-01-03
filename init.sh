#!/bin/bash

# 确保目录存在
mkdir -p data/posts data/images

# 初始化git仓库
git init

# 添加文件
git add .

# 创建初始提交
git commit -m "Initial commit"

# 设置main分支
git branch -M main

# 添加远程仓库（需要替换用户名）
echo "请输入您的GitHub用户名："
read username
git remote add origin "https://github.com/$username/$username.github.io.git"

# 推送到GitHub
echo "正在推送到GitHub..."
git push -u origin main

echo "初始化完成！"
echo "请访问 https://github.com/$username/$username.github.io/settings/pages"
echo "确保GitHub Pages已启用并设置为使用GitHub Actions"

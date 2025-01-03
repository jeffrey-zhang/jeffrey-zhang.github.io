// 使用 GitHub Issues 作为评论系统
document.addEventListener('DOMContentLoaded', function() {
    const commentsSection = document.getElementById('comments');
    if (!commentsSection) return;

    const postPath = window.location.pathname;
    const issueTitle = `Comments for ${postPath}`;
    const repo = 'jeffrey-zhang/jeffrey-zhang.github.io';
    const issuesUrl = `https://github.com/${repo}/issues`;

    // 添加评论链接
    const commentLink = document.createElement('a');
    commentLink.href = `${issuesUrl}/new?title=${encodeURIComponent(issueTitle)}`;
    commentLink.target = '_blank';
    commentLink.className = 'comment-link';
    commentLink.textContent = '发表评论';

    const commentHint = document.createElement('p');
    commentHint.className = 'comment-hint';
    commentHint.textContent = '评论功能由 GitHub Issues 提供，请使用 GitHub 账号登录后发表评论。';

    commentsSection.appendChild(commentHint);
    commentsSection.appendChild(commentLink);
});

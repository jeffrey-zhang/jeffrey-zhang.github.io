// 简单的搜索功能实现
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if (!searchInput || !searchResults) return;

    searchInput.addEventListener('input', debounce(function(e) {
        const query = e.target.value.toLowerCase().trim();
        
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }

        // 从预加载的文章数据中搜索
        const results = window.posts.filter(post => 
            post.title.toLowerCase().includes(query) ||
            post.content.toLowerCase().includes(query) ||
            post.category.toLowerCase().includes(query) ||
            post.tags.some(tag => tag.toLowerCase().includes(query))
        );

        displayResults(results);
    }, 300));

    function displayResults(results) {
        if (results.length === 0) {
            searchResults.innerHTML = '<p class="no-results">未找到相关文章</p>';
        } else {
            searchResults.innerHTML = results.map(post => `
                <article class="search-result">
                    <h3><a href="${post.url}">${post.title}</a></h3>
                    <div class="meta">
                        <time>${post.date}</time>
                        <span class="category">${post.category}</span>
                    </div>
                </article>
            `).join('');
        }
        searchResults.style.display = 'block';
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});

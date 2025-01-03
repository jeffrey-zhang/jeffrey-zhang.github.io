document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if (!searchInput || !searchResults) return;

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

    function search(query) {
        if (!window.posts) return [];
        
        query = query.toLowerCase();
        return window.posts.filter(post => {
            return post.title.toLowerCase().includes(query) ||
                   post.content.toLowerCase().includes(query) ||
                   post.category.toLowerCase().includes(query) ||
                   post.tags.some(tag => tag.toLowerCase().includes(query));
        });
    }

    function displayResults(results) {
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="search-result">没有找到相关文章</div>';
            return;
        }

        searchResults.innerHTML = results.map(post => `
            <div class="search-result">
                <h3><a href="${post.url}">${post.title}</a></h3>
                <div class="meta">
                    <time>${post.date}</time>
                    <span class="category">${post.category}</span>
                </div>
            </div>
        `).join('');
    }

    const debouncedSearch = debounce((query) => {
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }

        const results = search(query);
        displayResults(results);
        searchResults.style.display = 'block';
    }, 300);

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        debouncedSearch(query);
    });

    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
});

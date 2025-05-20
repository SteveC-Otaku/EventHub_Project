document.addEventListener('DOMContentLoaded', function() {
    // 从URL获取搜索参数
    const urlParams = new URLSearchParams(window.location.search);
    const origin = urlParams.get('origin') || '北京';
    const destination = urlParams.get('destination') || '上海';
    const departDate = urlParams.get('departDate') || '2023-06-15';
    const returnDate = urlParams.get('returnDate') || '';
    const passengers = urlParams.get('passengers') || '1';
    const tripType = urlParams.get('tripType') || 'roundTrip';
    
    // 更新页面上的搜索信息
    document.getElementById('origin-display').textContent = origin;
    document.getElementById('destination-display').textContent = destination;
    document.getElementById('date-display').textContent = departDate;
    document.getElementById('passengers-display').textContent = `${passengers} 位乘客`;
    
    // 如果是单程，隐藏返程标签
    if (tripType === 'oneWay') {
        const returnTab = document.querySelector('[data-tab="return"]');
        if (returnTab) {
            returnTab.style.display = 'none';
        }
    }
    
    // 修改搜索按钮点击事件
    const modifySearchButton = document.querySelector('.modify-search');
    if (modifySearchButton) {
        modifySearchButton.addEventListener('click', function() {
            window.location.href = `index.html?origin=${origin}&destination=${destination}&departDate=${departDate}&returnDate=${returnDate}&passengers=${passengers}&tripType=${tripType}`;
        });
    }
    
    // 航班详情切换
    const detailsToggleButtons = document.querySelectorAll('.details-toggle');
    detailsToggleButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const card = this.closest('.flight-card');
            const details = card.querySelector('.flight-features');
            
            if (details.style.display === 'none' || details.style.display === '') {
                details.style.display = 'flex';
                this.textContent = '隐藏详情';
            } else {
                details.style.display = 'none';
                this.textContent = '查看详情';
            }
        });
    });
    
    // 初始化时隐藏所有航班详情
    document.querySelectorAll('.flight-features').forEach(function(details) {
        details.style.display = 'none';
    });
    
    // 排序功能
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sortValue = this.value;
            const flightList = document.querySelector('.flight-list');
            const flightCards = Array.from(flightList.querySelectorAll('.flight-card'));
            
            flightCards.sort(function(a, b) {
                if (sortValue === 'price-asc') {
                    const priceA = parseInt(a.querySelector('.price').textContent.replace(/[^0-9]/g, ''));
                    const priceB = parseInt(b.querySelector('.price').textContent.replace(/[^0-9]/g, ''));
                    return priceA - priceB;
                } else if (sortValue === 'price-desc') {
                    const priceA = parseInt(a.querySelector('.price').textContent.replace(/[^0-9]/g, ''));
                    const priceB = parseInt(b.querySelector('.price').textContent.replace(/[^0-9]/g, ''));
                    return priceB - priceA;
                } else if (sortValue === 'time-asc') {
                    const timeA = a.querySelector('.departure .time').textContent;
                    const timeB = b.querySelector('.departure .time').textContent;
                    return timeA.localeCompare(timeB);
                } else if (sortValue === 'duration-asc') {
                    const durationA = a.querySelector('.duration').textContent;
                    const durationB = b.querySelector('.duration').textContent;
                    // 简单比较，实际应该转换为分钟数
                    return durationA.localeCompare(durationB);
                }
                return 0;
            });
            
            // 重新添加排序后的航班卡片
            flightCards.forEach(function(card) {
                flightList.appendChild(card);
            });
        });
    }
    
    // 筛选功能
    const filterButtons = document.querySelectorAll('.filter-button');
    filterButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // 这里只是示例，实际应该根据筛选条件过滤航班
            button.classList.toggle('active');
            alert('筛选功能将在实际应用中实现');
        });
    });
});
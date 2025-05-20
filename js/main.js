// 移动菜单切换
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');

    if (mobileMenuToggle && mobileNav) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileNav.style.display = mobileNav.style.display === 'block' ? 'none' : 'block';
            mobileMenuToggle.innerHTML = mobileNav.style.display === 'block' ? 
                '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
        });
    }

    // 移动下拉菜单
    const mobileDropdowns = document.querySelectorAll('.mobile-dropdown');
    
    mobileDropdowns.forEach(function(dropdown) {
        const dropdownLink = dropdown.querySelector('a');
        
        dropdownLink.addEventListener('click', function(e) {
            e.preventDefault();
            dropdown.classList.toggle('active');
            const icon = dropdownLink.querySelector('i');
            icon.className = dropdown.classList.contains('active') ? 
                'fas fa-chevron-up' : 'fas fa-chevron-down';
        });
    });

    // 标签切换
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            const tabContent = document.getElementById(tabId + '-tab');
            
            if (tabContent) {
                // 移除所有标签和内容的活动状态
                document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
                
                // 添加当前标签和内容的活动状态
                this.classList.add('active');
                tabContent.classList.add('active');
            }
        });
    });

    // 设置当前年份
    const currentYearElements = document.querySelectorAll('#current-year');
    currentYearElements.forEach(function(element) {
        element.textContent = new Date().getFullYear();
    });
});

// 航班搜索表单处理
document.addEventListener('DOMContentLoaded', function() {
    const flightSearchForm = document.getElementById('flight-search-form');
    const tripTypeRadios = document.querySelectorAll('input[name="trip-type"]');
    const returnDateGroup = document.getElementById('return-date-group');
    const swapLocationsButton = document.getElementById('swap-locations');
    const originInput = document.getElementById('origin');
    const destinationInput = document.getElementById('destination');

    if (flightSearchForm) {
        // 单程/往返切换
        tripTypeRadios.forEach(function(radio) {
            radio.addEventListener('change', function() {
                if (this.value === 'oneWay') {
                    returnDateGroup.style.display = 'none';
                } else {
                    returnDateGroup.style.display = 'block';
                }
            });
        });

        // 交换出发地和目的地
        if (swapLocationsButton && originInput && destinationInput) {
            swapLocationsButton.addEventListener('click', function() {
                const temp = originInput.value;
                originInput.value = destinationInput.value;
                destinationInput.value = temp;
            });
        }

        // 表单提交
        flightSearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const origin = originInput.value;
            const destination = destinationInput.value;
            const departDate = document.getElementById('depart-date').value;
            const returnDate = document.getElementById('return-date')?.value || '';
            const passengers = document.getElementById('passengers').value;
            const tripType = document.querySelector('input[name="trip-type"]:checked').value;
            
            // 构建URL参数
            const params = new URLSearchParams();
            params.append('origin', origin);
            params.append('destination', destination);
            params.append('departDate', departDate);
            if (returnDate) params.append('returnDate', returnDate);
            params.append('passengers', passengers);
            params.append('tripType', tripType);
            
            // 跳转到航班搜索结果页
            window.location.href = `flights.html?${params.toString()}`;
        });
    }
});
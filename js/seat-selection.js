document.addEventListener('DOMContentLoaded', function() {
    // 座位状态类型
    const SeatStatus = {
        AVAILABLE: 'available',
        OCCUPIED: 'occupied',
        SELECTED: 'selected',
        PREMIUM: 'premium',
        EXIT: 'exit'
    };

    // 座位价格
    const SeatPrices = {
        [SeatStatus.AVAILABLE]: 50,
        [SeatStatus.PREMIUM]: 120,
        [SeatStatus.EXIT]: 80
    };

    // 生成座位数据
    function generateSeats() {
        const rows = 30;
        const seatsPerRow = 6;
        const seats = [];

        for (let row = 1; row <= rows; row++) {
            const seatRow = [];
            for (let seat = 0; seat < seatsPerRow; seat++) {
                const seatLetter = String.fromCharCode(65 + seat);
                const seatId = `${row}${seatLetter}`;

                // 随机生成座位状态，但保持一定比例的可用座位
                let status = SeatStatus.AVAILABLE;
                const random = Math.random();

                if (row <= 5) {
                    status = SeatStatus.PREMIUM; // 前几排是高级座位
                } else if (row === 15 || row === 16) {
                    status = SeatStatus.EXIT; // 安全出口座位
                } else if (random < 0.3) {
                    status = SeatStatus.OCCUPIED; // 30%的座位已被占用
                }

                // 设置座位价格
                let price = SeatPrices[status] || SeatPrices[SeatStatus.AVAILABLE];

                seatRow.push({ id: seatId, status, price });
            }
            seats.push(seatRow);
        }

        return seats;
    }

    // 渲染座位图
    function renderSeatMap(seats) {
        const seatGrid = document.getElementById('seat-grid');
        if (!seatGrid) return;

        seatGrid.innerHTML = '';

        seats.forEach((row, rowIndex) => {
            const seatRow = document.createElement('div');
            seatRow.className = 'seat-row';

            // 行号
            const rowNumber = document.createElement('div');
            rowNumber.className = 'row-number';
            rowNumber.textContent = rowIndex + 1;
            seatRow.appendChild(rowNumber);

            // 座位
            const seatsContainer = document.createElement('div');
            seatsContainer.className = 'seats';

            row.forEach((seat, seatIndex) => {
                const seatElement = document.createElement('div');
                seatElement.className = `seat ${seat.status}`;
                seatElement.textContent = seat.id;
                seatElement.dataset.row = rowIndex;
                seatElement.dataset.seat = seatIndex;
                seatElement.title = getSeatTooltip(seat);

                if (seat.status !== SeatStatus.OCCUPIED) {
                    seatElement.addEventListener('click', () => handleSeatClick(rowIndex, seatIndex));
                }

                seatsContainer.appendChild(seatElement);
            });

            seatRow.appendChild(seatsContainer);

            // 行号（右侧）
            const rowNumberRight = document.createElement('div');
            rowNumberRight.className = 'row-number';
            rowNumberRight.textContent = rowIndex + 1;
            seatRow.appendChild(rowNumberRight);

            seatGrid.appendChild(seatRow);
        });
    }

    // 获取座位提示文本
    function getSeatTooltip(seat) {
        if (seat.status === SeatStatus.OCCUPIED) {
            return '已被占用';
        } else if (seat.status === SeatStatus.PREMIUM) {
            return `高级座位 - ¥${seat.price}`;
        } else if (seat.status === SeatStatus.EXIT) {
            return `安全出口座位 - ¥${seat.price}`;
        } else {
            return `标准座位 - ¥${seat.price}`;
        }
    }

    // 更新选中座位显示
    function updateSelectedSeats(selectedSeats) {
        const container = document.getElementById('selected-seats-container');
        if (!container) return;

        if (selectedSeats.length === 0) {
            container.innerHTML = '<p class="empty-selection">您尚未选择任何座位</p>';
            return;
        }

        const selectedSeatsHTML = document.createElement('div');
        selectedSeatsHTML.className = 'selected-seats';

        selectedSeats.forEach(seat => {
            const seatTag = document.createElement('div');
            seatTag.className = 'selected-seat-tag';
            seatTag.textContent = seat.id;
            selectedSeatsHTML.appendChild(seatTag);
        });

        container.innerHTML = '';
        container.appendChild(selectedSeatsHTML);
    }

    // 计算选中座位的总价
    function calculateTotalPrice(selectedSeats) {
        return selectedSeats.reduce((total, seat) => total + seat.price, 0);
    }

    // 更新价格显示
    function updatePriceDisplay(price) {
        const priceElement = document.getElementById('seat-price-total');
        const sidebarPriceElement = document.getElementById('sidebar-seat-fee');
        const totalPriceElement = document.getElementById('total-price');

        if (priceElement) {
            priceElement.textContent = `¥${price}`;
        }

        if (sidebarPriceElement) {
            sidebarPriceElement.textContent = `¥${price}`;
        }

        if (totalPriceElement) {
            // 基本价格 + 税费 + 服务费 + 座位费
            const basePrice = 880;
            const taxFee = 120;
            const serviceFee = 50;
            const totalPrice = basePrice + taxFee + serviceFee + price;
            totalPriceElement.textContent = `¥${totalPrice}`;
        }
    }

    // 座位点击处理
    let seats = generateSeats();
    let selectedSeats = [];

    function handleSeatClick(rowIndex, seatIndex) {
        const seat = seats[rowIndex][seatIndex];

        if (seat.status === SeatStatus.OCCUPIED) return;

        if (seat.status === SeatStatus.SELECTED) {
            // 取消选择
            const originalStatus = seat.originalStatus || SeatStatus.AVAILABLE;
            seat.status = originalStatus;
            selectedSeats = selectedSeats.filter(s => s.id !== seat.id);
        } else {
            // 选择座位
            seat.originalStatus = seat.status; // 保存原始状态
            seat.status = SeatStatus.SELECTED;
            selectedSeats.push(seat);
        }

        // 更新UI
        renderSeatMap(seats);
        updateSelectedSeats(selectedSeats);
        updatePriceDisplay(calculateTotalPrice(selectedSeats));
    }

    // 初始化座位选择
    if (document.getElementById('seat-grid')) {
        renderSeatMap(seats);
        updateSelectedSeats(selectedSeats);
        updatePriceDisplay(calculateTotalPrice(selectedSeats));
    }
});
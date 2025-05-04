document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.qty-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const inputId = this.dataset.input;
            const input = document.getElementById(inputId);
            const currentValue = parseInt(input.value) || 0;

            if (this.dataset.action === 'increase') {
                input.value = currentValue + 1;
            } else if (this.dataset.action === 'decrease' && currentValue > 0) {
                input.value = currentValue - 1;
            }
        });
    });

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const searchTerm = this.value.toLowerCase();
            const table = document.getElementById('inventoryTable');

            if (table) {
                const rows = table.querySelectorAll('tbody tr');

                rows.forEach(row => {
                    const productName = row.querySelector('td:first-child').textContent.toLowerCase();
                    row.style.display = productName.includes(searchTerm) ? '' : 'none';
                });
            }
        });
    }
});

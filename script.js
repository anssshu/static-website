document.addEventListener('DOMContentLoaded', function() {
    fetch('data.xlsx')
        .then(response => response.arrayBuffer())
        .then(data => {
            const workbook = XLSX.read(data, { type: 'array' });
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            const json = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

            const table = document.getElementById('data-table');
            json.forEach((row, rowIndex) => {
                const tr = document.createElement('tr');
                row.forEach(cell => {
                    const cellElement = rowIndex === 0 ? document.createElement('th') : document.createElement('td');
                    cellElement.textContent = cell;
                    tr.appendChild(cellElement);
                });
                table.appendChild(tr);
            });
        });
});

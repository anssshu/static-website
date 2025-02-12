fetch('data.json')
  .then(response => response.json())
  .then(data => {
    const headers = data.headers;
    const rows = data.rows;

    const tableHeaders = document.getElementById('table-headers');
    headers.forEach(header => {
      const th = document.createElement('th');
      th.textContent = header;
      tableHeaders.appendChild(th);
    });

    const tableRows = document.getElementById('table-rows');
    rows.forEach(row => {
      const tr = document.createElement('tr');
      row.forEach(cell => {
        const td = document.createElement('td');
        td.textContent = cell;
        tr.appendChild(td);
      });
      tableRows.appendChild(tr);
    });
  })
  .catch(error => console.error('Error fetching data:', error));

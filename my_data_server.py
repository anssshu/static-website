import pandas as pd
import json
import http.server
import socketserver
import webbrowser
import threading
import msvcrt
import os

# Get the correct path of the data.xlsx file
current_dir = os.path.dirname(os.path.abspath(__file__))
excel_file_path = os.path.join(current_dir, 'data.xlsx')

# Read the Excel file
df = pd.read_excel(excel_file_path, header=None)

# Replace NaN values with empty strings
df = df.fillna('')

# Convert the DataFrame to a list of lists
data = df.values.tolist()  

# Extract headers and rows
headers = data[0]
rows = data[1:]

# Create a dictionary to hold the data
data_dict = {
    "headers": headers,
    "rows": rows
}

# Write the data to a JSON file with utf-8 encoding
json_file_path = os.path.join(current_dir, 'data.json')
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_dict, json_file, indent=2, ensure_ascii=False)

print('Data has been written to data.json')

# Generate the index.html file
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display JSON Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #006400;  /* Dark green color */
            color: white;
        }
    </style>
</head>
<body>
    <h1></h1>
    <table id="data-table">
        <thead>
            <tr id="table-headers"></tr>
        </thead>
        <tbody id="table-rows"></tbody>
    </table>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
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
                .catch(error => console.error('Error fetching JSON data:', error));
        });
    </script>
</body>
</html>'''

html_file_path = os.path.join(current_dir, 'index.html')
with open(html_file_path, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print('index.html has been generated')

# Define the handler to serve the HTML file
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve files from the current directory
        return os.path.join(current_dir, path.lstrip('/'))

# Define the server
PORT = 8000
httpd = socketserver.TCPServer(('', PORT), CustomHTTPRequestHandler)

# Function to start the server
def start_server():
    print(f'Serving at port {PORT}')
    webbrowser.open(f'http://localhost:{PORT}/index.html')
    httpd.serve_forever()

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Wait for the ESC key to stop the server
print('Press ESC to stop the server')
while True:
    if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':  # ESC key
        print('Stopping the server...')
        httpd.shutdown()
        server_thread.join()
        break
print('Server stopped')

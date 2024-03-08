from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import json
import mysql.connector

# Database connection setup
cnx = mysql.connector.connect(
    host='db',
    user='root',
    password='my_root_pass',
    database='my_database',
    port=3306
)
cursor = cnx.cursor()

# Create HEALTH table if not exists
table_description = (
    "CREATE TABLE IF NOT EXISTS `HEALTH` ("
    "  `HEALTH_ID` INT AUTO_INCREMENT NOT NULL,"
    "  `STATUS` VARCHAR(14) NOT NULL,"
    "  `DESCRIPTION` VARCHAR(50) NOT NULL,"
    "  PRIMARY KEY (`HEALTH_ID`))"
)
cursor.execute(table_description)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Respond with a default message for the root path
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, World! This is your PHR system.')
        elif self.path == '/health_records':
            # Fetch health records from the database
            cursor.execute("SELECT * FROM HEALTH")
            records = cursor.fetchall()

            # Create a JSON response with the fetched records
            response_content = json.dumps(records)

            # Send the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_content.encode('utf-8'))
        else:
            # Respond with a 404 Not Found for unknown paths
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        if self.path == '/health_records':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            # Example: Insert data into the database
            insert_query = "INSERT INTO HEALTH (STATUS, DESCRIPTION) VALUES (%s, %s)"
            insert_values = (data.get('status'), data.get('description'))

            cursor.execute(insert_query, insert_values)
            cnx.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = BytesIO()
            response.write(b'{"message": "Health record added successfully"}')
            self.wfile.write(response.getvalue())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_PUT(self):
        if self.path.startswith('/health_records/'):
            # Extract record ID from the URL
            record_id = int(self.path.split('/')[-1])

            # Parse JSON body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            # Example: Update data in the database
            update_query = "UPDATE HEALTH SET STATUS=%s, DESCRIPTION=%s WHERE HEALTH_ID=%s"
            update_values = (data.get('status'), data.get('description'), record_id)

            cursor.execute(update_query, update_values)
            cnx.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = BytesIO()
            response.write(b'{"message": "Health record updated successfully"}')
            self.wfile.write(response.getvalue())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_DELETE(self):
        if self.path.startswith('/health_records/'):
            # Extract record ID from the URL
            record_id = int(self.path.split('/')[-1])

            # Example: Delete data from the database
            delete_query = "DELETE FROM HEALTH WHERE HEALTH_ID=%s"
            delete_values = (record_id,)

            cursor.execute(delete_query, delete_values)
            cnx.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = BytesIO()
            response.write(b'{"message": "Health record deleted successfully"}')
            self.wfile.write(response.getvalue())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()



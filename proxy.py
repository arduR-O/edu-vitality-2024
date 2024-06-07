import http.server
import socketserver
import requests

# Define the target server
TARGET_HOST = '172.17.5.48'
TARGET_PORT = 8081

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.forward_request()

    def do_POST(self):
        self.forward_request()

    def do_PUT(self):
        self.forward_request()

    def do_DELETE(self):
        self.forward_request()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def forward_request(self):
        # Construct the full URL for the target server
        url = f'http://{TARGET_HOST}:{TARGET_PORT}{self.path}'

        # Forward the headers, excluding the Origin header
        headers = {key: value for key, value in self.headers.items() if key.lower() != 'origin'}

        # Forward the request method and data
        if self.command in ['POST', 'PUT']:
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
            response = requests.request(self.command, url, headers=headers, data=data)
        else:
            response = requests.request(self.command, url, headers=headers)

        # Print the response details
        print(f'Response Status: {response.status_code}')
        print('Response Headers:')
        for key, value in response.headers.items():
            print(f'  {key}: {value}')
        print('Response Content:')
        print(response.text)

        # Send the response back to the client
        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(response.content)

def run(server_class=http.server.HTTPServer, handler_class=ProxyHTTPRequestHandler):
    server_address = ('', 8081)
    httpd = server_class(server_address, handler_class)
    print('Starting proxy on port 8081...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

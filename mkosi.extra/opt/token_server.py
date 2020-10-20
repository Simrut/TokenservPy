#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl, datetime, python_jwt as jwt, jwcrypto.jwk as jwk

def write_key():
    f = open('key.pem', 'w')
    key = jwk.JWK.generate(kty='RSA', size=2048)
    f.write(str(key.export_to_pem(True, None)))

def create_jwt():
    f = open("HMAC_key.pem", "rb")
    key = jwk.JWK.from_pem(f.read())
    payload = { 'pay': 'load', 'bimmbammbumm': 90 };
    token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(weeks=4))
    return token

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':

            token = create_jwt()

            self.send_response(200)
            self.send_header('Content-type',  'text/html')
            self.end_headers()
            self.wfile.write(bytes(token, encoding='utf8'))
        

httpd = HTTPServer(('localhost', 8443), MyHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='cert_key.pem', server_side=True)

httpd.serve_forever()
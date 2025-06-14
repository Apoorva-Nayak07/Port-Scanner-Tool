from flask import Flask, render_template, request, Response
import socket
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    target = data['target']
    start_port = int(data['start_port'])
    end_port = int(data['end_port'])

    def generate():
        for port in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((target, port))
                if result == 0:
                    yield f'<span style="color:lime;">✅ Port {port} is OPEN</span><br>\n'
                else:
                    yield f'<span style="color:red;">❌ Port {port} is CLOSED</span><br>\n'
                time.sleep(0.05)  # Small delay for better display flow

    return Response(generate(), mimetype='text/html')

if __name__ == '__main__':
 import os
 port = int(os.environ.get("PORT", 5000))
 app.run(host="0.0.0.0", port=port)


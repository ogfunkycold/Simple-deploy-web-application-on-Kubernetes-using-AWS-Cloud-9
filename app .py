from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route("/")
def Testhello():
    html="<h1>Hello {name}!</h1>" \
         "<h3>Hostname:</h3> {hostname}<br/>"\
         "<h3>Version:</h3> First Kubernetes Deployment<br/>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
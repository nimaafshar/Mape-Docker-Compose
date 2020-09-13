from flask import Flask
from flask import request
import subprocess

app = Flask(__name__)
docker_compose_path ='../docker-compose.yml'

@app.route('/<container>/<int:replicas>')
def home(container,replicas):
    p = subprocess.Popen(["docker-compose", "-f",docker_compose_path, "up" ,"-d" ,"--scale", f"{container}={replicas}"],
                        shell=True,
                        stdout=subprocess.PIPE,
                        close_fds=True,
                        stderr=subprocess.STDOUT)
    return p.stdout.read()
    


if __name__ == '__main__':
    app.run(host="localhost",port=5522,debug=True)
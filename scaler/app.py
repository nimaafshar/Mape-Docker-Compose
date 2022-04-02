import os
import pathlib
import subprocess

from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

SERVICE_NAME = os.environ.get('SCALER_SERVICE_NAME')
DOCKER_COMPOSE_PATH = pathlib.Path(os.environ.get('SCALER_COMPOSE_PATH'))

app: Flask = Flask(__name__)


@app.route('/scale', methods=['POST'])
def scale():
    """
    scales SERVICE_NAME service in docker compose located in DOCKER_COMPOSE_PATH
    to given number of replicas from json data
    example json:
        {
            "replicas": 2
        }
    """
    request_data: dict = request.get_json(silent=True)
    replicas = request_data.get('replicas')
    if request_data is None or replicas is None or not isinstance(replicas, int):
        return {'status': 'fail', 'error': 'bad request format'}, 400
    else:
        response: dict = {}
        status_code: int = 200
        result: subprocess.CompletedProcess = subprocess.run(
            ['sudo', 'docker-compose', '-f', DOCKER_COMPOSE_PATH, 'up', ' -d', '--scale',
             f'{SERVICE_NAME} = {replicas}'], capture_output=True)
        if result.returncode != 0:
            status_code = 400
            response['status'] = 'fail'
        else:
            response['status'] = 'success'
        response['stdout'] = result.stdout
        response['stderr'] = result.stderr
        return result, status_code


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

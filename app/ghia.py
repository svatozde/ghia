from flask import Flask
from flask import request
from flask import logging
import json
import hmac
import hashlib

app = Flask(__name__)

hooks = []
invalid_hooks = []

w_secret = 'WjMTejwojlt7wfZw3PB3'


def is_valid_signature(x_hub_signature, data, private_key):
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)




@app.route('/', methods=['POST'])
def gitHub():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_json(force=True))

    x_hub_signature = request.headers.get('X-Hub-Signature')

    hooks.append(x_hub_signature)

    app.logger.info("x_hub_signature:" + x_hub_signature)

    if is_valid_signature(x_hub_signature, request.data, w_secret):
        app.logger.info(x_hub_signature + " is valid!")
        hooks.append(request.get_json(force=True))
    else:
        invalid_hooks.append(request.get_json(force=True))

    return 'ok'


@app.route('/hooks')
def index():
    return "Hello World! </br> Valid hook:" + json.dumps(hooks) + \
           " </br>   Invalid hooks:" + json.dumps(invalid_hooks)


if __name__ == '__main__':
    app.run()

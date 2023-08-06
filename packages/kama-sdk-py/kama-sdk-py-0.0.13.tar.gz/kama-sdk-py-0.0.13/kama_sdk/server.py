import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from k8kat.auth.kube_broker import BrokerConnException

from kama_sdk.controllers import operations_controller, status_controller, \
  app_controller, variables_controller, releases_controller, \
  telem_controller, injections_controller, actions_controller, concerns_controller, plugins_controller
from kama_sdk.core.core import utils
from kama_sdk.core.core.config_man import coerce_ns

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

controllers = [
  status_controller,
  operations_controller,
  app_controller,
  concerns_controller,
  telem_controller,
  releases_controller,
  variables_controller,
  injections_controller,
  actions_controller,
  plugins_controller
]

for controller in controllers:
  app.register_blueprint(controller.controller)


CORS(app)


@app.errorhandler(BrokerConnException)
def all_exception_handler(error):
  return jsonify(dict(
    error='could not connect to Kubernetes API',
    reason=str(error)
  )), 500


@app.before_request
def read_dev_ns():
  coerced_ns = request.headers.get('Appns')
  if coerced_ns:
    if utils.is_out_of_cluster():
      coerce_ns(coerced_ns)
    else:
      print(f"[kama_sdk::server] set-ns from header env={utils.run_env()}!")


def start():
  app.config["cmd"] = ["bash"]
  app.config['JSON_SORT_KEYS'] = False
  app.run(host='0.0.0.0', port=5000, extra_files=['./**/*.yaml'])

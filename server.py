import argparse
import json
import logging
import os
import simplejson
from functools import wraps
import urllib.parse
from klein import Klein
from logits import utils
from twisted.web.static import File

from logits.ssr2json import text2cfg

logger = logging.getLogger(__name__)

version = '0.0.1'


def create_argument_parser():
    parser = argparse.ArgumentParser(description='parse incoming text')
    parser.add_argument('-P', "--port", type=int, default=5000, help='port on which to run server')
    return parser


def decode_parameters(request):
    """Make sure all the parameters have the same encoding."""

    return {
        key.decode('utf-8', 'strict'): value[0].decode('utf-8', 'strict')
        for key, value in request.args.items()}


def parameter_or_default(request, name, default=None):
    """Return a parameters value if part of the request, or the default."""

    request_params = decode_parameters(request)
    return request_params.get(name, default)


def dump_to_data_file(data):
    if isinstance(data, str):
        data_string = data
    else:
        data_string = utils.json_to_string(data)

    return utils.create_temporary_file(data_string, "_training_data")


class ConvertServer(object):
    """Class representing Rasa NLU http server"""

    app = Klein()

    def __init__(self):
        pass

    @app.route("/", methods=['GET', 'OPTIONS'])
    def hello(self, request):
        """Main Rasa route to check if the server is online"""
        return File("./templates/ssr.html")

    @app.route("/index", methods=['GET', 'OPTIONS'])
    def index(self, request):
        """
        返回SSR 解析Form框
        :param request:
        :return:
        """
        return File("./templates/ssr.html")

    @app.route("/ssr2json", methods=['POST'])
    def ssr2json(self, request):
        """
        返回SSR 解析Form框
        :param request:
        :return:
        """
        request.setHeader('Content-Type', 'application/json')
        if request.method.decode('utf-8', 'strict') == 'GET':
            request_params = decode_parameters(request)
        else:
            text = request.content.read().decode('utf-8', 'strict')
            request_params = {token.split('=')[0]: token.split('=')[1] for token in text.split('&')}

        if 'text' in request_params:
            cfg = text2cfg(request_params.get('text', None))
        else:
            cfg = {}
        response = json.dumps(cfg, indent=4)
        return response

    @app.route("/version", methods=['GET', 'OPTIONS'])
    def version(self, request):
        """Returns the Rasa server's version"""

        request.setHeader('Content-Type', 'application/json')
        return utils.json_to_string({'version': version})

    @app.route('/static/', branch=True)
    def static(self, request):
        return File("./static")


def get_token(_clitoken: str) -> str:
    _envtoken = os.environ.get("RASA_NLU_TOKEN")

    if _clitoken and _envtoken:
        raise Exception(
            "RASA_NLU_TOKEN is set both with the -t option,"
            " with value `{}`, and with an environment variable, "
            "with value `{}`. "
            "Please set the token with just one method "
            "to avoid unexpected behaviours.".format(
                _clitoken, _envtoken))

    token = _clitoken or _envtoken
    return token


def main(args):
    server = ConvertServer()
    logger.info('Started http server on port %s' % args.port)
    server.app.run('0.0.0.0', args.port)


if __name__ == '__main__':
    # Running as standalone python application
    cmdline_args = create_argument_parser().parse_args()
    main(cmdline_args)

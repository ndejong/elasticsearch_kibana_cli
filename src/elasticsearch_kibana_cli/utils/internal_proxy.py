
import os
import logging
import requests
from flask import Flask, Response, request


class ElasticsearchKibanaCLIInternalProxy:

    debug = False
    listen_port = 59200
    listen_proto = 'http'
    listen_address = '127.0.0.1'
    header_overrides = {}
    request_methods = ['GET', 'POST']

    client_connect_address = None

    def __init__(self, config):

        for config_k, config_v in config.items():
            if config_k.lower() == 'header_overrides':
                self.header_overrides = config_v
            elif config_k.lower() == 'listen':
                if 'address' in config_v.keys():
                    self.listen_address = config_v['address']
                if 'port' in config_v.keys():
                    self.listen_port = config_v['port']
                if 'proto' in config_v.keys():
                    self.listen_proto = config_v['proto']
            elif config_k.lower() == 'debug' and str(config_v).lower() in ['yes', 'true', 'on', '1']:
                self.debug = True

        self.client_connect_address = '{}://{}:{}'.format(self.listen_proto, self.listen_address, self.listen_port)

    def start(self, base_uri):

        app = Flask('ElasticsearchKibanaCLIInternalProxy')

        if not self.debug:
            os.environ['WERKZEUG_RUN_MAIN'] = 'true'
            logger = logging.getLogger('werkzeug')
            logger.disabled = True

        @app.route('/<path:path>', methods=self.request_methods)
        @app.route('/', defaults={'path': None}, methods=self.request_methods)
        def catchall(path):

            method = request.method
            path = request.full_path
            data = request.get_data(cache=False, as_text=False, parse_form_data=False)

            headers = {}
            headers_replaced = []
            for header in str(request.headers).split('\r\n'):
                if ': ' in header:
                    header_k, header_v = header.split(': ', 1)
                    if header_k.lower() in self.header_overrides.keys():
                        headers[header_k.lower()] = self.header_overrides[header_k.lower()]
                        headers_replaced.append(header_k.lower())
                    else:
                        headers[header_k.lower()] = header_v

            for header_k in self.header_overrides.keys():
                if header_k.lower() not in headers_replaced:
                    headers[header_k.lower()] = self.header_overrides[header_k]

            if 'cookie' in headers.keys():
                headers['cookie'] = headers['cookie'].replace('cookie: ','').replace('Cookie: ','').strip()

            if base_uri[-1:] == '/' and path[:1] == '/':
                url = '{}{}'.format(base_uri, path[1:])
            elif base_uri[-1:] != '/' and path[:1] != '/':
                url = '{}/{}'.format(base_uri, path)
            else:
                url = '{}{}'.format(base_uri, path)

            # print([url, headers, data])
            r = requests.request(method, url=url, headers=headers, data=data, stream=True)
            return Response(r.content, status=r.status_code)

        app.run(host=self.listen_address, port=self.listen_port, threaded=True, debug=False)

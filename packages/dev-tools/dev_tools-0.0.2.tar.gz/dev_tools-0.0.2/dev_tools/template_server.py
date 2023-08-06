#! /bin/env python3
import argparse
import json
import os

from flask import Flask
from jinja2 import Template


def _parse_args():
    parser = argparse.ArgumentParser(prog='passer_template_server',
                                     description='模板开发工具')
    parser.add_argument(
        'template', help='模板文件路径, eg: test-data/src/template.html')
    parser.add_argument(
        'parameter', help='参数文件路径, eg: test-data/parameter.json')
    return parser.parse_args()

def _main():
    args = _parse_args()
    template_path = args.template
    parameter_path = args.parameter

    static_folder = os.path.abspath(os.path.dirname(template_path))
    print('The static folder: ', static_folder)
    app = Flask(__name__, static_folder=static_folder, static_url_path='')

    @app.route('/template.html')
    def serve_template():
        parameter = json.load(open(parameter_path, 'rb'))
        with open(template_path, 'r', encoding='utf-8') as template_src:
            template = Template(template_src.read())
        print("Rendering parameters got: ", parameter)
        return template.render(data=parameter)

    app.run(debug=True)


if __name__ == '__main__':
    _main()

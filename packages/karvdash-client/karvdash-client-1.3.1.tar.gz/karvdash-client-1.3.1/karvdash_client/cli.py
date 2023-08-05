# Copyright [2019] [FORTH-ICS]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import argparse

from pprint import pprint

from .api import API


def cmd_list_services(api, args):
    pprint(api.list_services())

def cmd_create_service(api, args):
    variables = dict(map(lambda s: s.split('='), args.variables))
    pprint(api.create_service(args.id, variables))

def cmd_exec_service(api, args):
    if not args.args:
        return
    response = api.exec_service(args.name, args.args, args.all_pods)
    sys.stdout.write(''.join(response['result'])) # No newline at the end

def cmd_delete_service(api, args):
    api.delete_service(args.name)

def cmd_list_templates(api, args):
    pprint(api.list_templates())

def cmd_add_template(api, args):
    with open(args.filename, 'rb') as fp:
        pprint(api.add_template(fp.read()))

def cmd_get_template(api, args):
    sys.stdout.write(api.get_template(args.id)['data'])

def cmd_remove_template(api, args):
    api.remove_template(args.id)

def main(cmd=None):
    parser = argparse.ArgumentParser(description='Karvdash API client command line tool')
    # parser.add_argument('-d', '--debug', action='store_true', help='Print debug info')
    parser.add_argument('--config', help='Karvdash API client configuration file')
    subprasers = parser.add_subparsers(dest='command', title='API command')

    list_services = subprasers.add_parser('list_services', help='List running services')
    list_services.set_defaults(func=cmd_list_services)

    create_service = subprasers.add_parser('create_service', help='Create/start a service')
    create_service.add_argument('id', help='Template identifier')
    create_service.add_argument('variables', nargs='+', help='Template variables as key=value pairs (provide at least a "name")')
    create_service.set_defaults(func=cmd_create_service)

    exec_service = subprasers.add_parser('exec_service', help='Execute a command at service pods')
    exec_service.add_argument('-a', '--all-pods', action='store_true', help='Execute in all pods')
    exec_service.add_argument('name', help='Service name')
    exec_service.add_argument('args', nargs=argparse.REMAINDER, help='Command and arguments to execute')
    exec_service.set_defaults(func=cmd_exec_service)

    delete_service = subprasers.add_parser('delete_service', help='Delete/stop a running service')
    delete_service.add_argument('name', help='Service name')
    delete_service.set_defaults(func=cmd_delete_service)

    list_templates = subprasers.add_parser('list_templates', help='List available templates')
    list_templates.set_defaults(func=cmd_list_templates)

    add_template = subprasers.add_parser('add_template', help='Add a template')
    add_template.add_argument('filename', help='Template filename')
    add_template.set_defaults(func=cmd_add_template)

    get_template = subprasers.add_parser('get_template', help='Get template data')
    get_template.add_argument('id', help='Template identifier')
    get_template.set_defaults(func=cmd_get_template)

    remove_template = subprasers.add_parser('remove_template', help='Remove a template')
    remove_template.add_argument('id', help='Template identifier')
    remove_template.set_defaults(func=cmd_remove_template)

    args = parser.parse_args(cmd)
    if args.command:
        api = API(args.config)
        args.func(api, args)
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

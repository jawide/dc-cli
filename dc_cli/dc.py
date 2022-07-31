import os
import sys
import time
import http
import shlex
import shutil
import urllib3
import textwrap
import argparse
import subprocess
import urllib.parse


DC_HOST = os.environ.get('DC_HOST')
DC_PACKAGE_PATH = os.environ.get('DC_PACKAGE_PATH')
DC_DOCKER_COMPOSE = os.environ.get('DC_DOCKER_COMPOSE')

HOST = DC_HOST or 'http://api.dc.jawide.top'
if sys.platform == 'win32':
    HOME = os.environ['USERPROFILE']
elif sys.platform in ['linux', 'darwin']:
    HOME = os.environ['HOME']
else:
    HOME = '.'
PACKAGE_PATH = os.environ.get('DC_PACKAGE_PATH') or os.path.join(HOME, '.dc/package')
DOCKER_COMPOSE = ''


def get_package_path(package) -> str:
    return os.path.join(PACKAGE_PATH, package)

def download_package(package):
    res = urllib3.PoolManager().request('GET', urllib.parse.urljoin(HOST, '/software/{}'.format(package)))
    if res.status == http.HTTPStatus.OK:
        dirpath = get_package_path(package)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        with open(os.path.join(dirpath, 'docker-compose.yml'), 'wb') as file:
            file.write(res.data)
    else:
        raise Exception('{}\nPackage {} download failed'.format(res.data, package))

def execute_docker_compose(dirpath, cmd, interval=0.1):
    code = subprocess.Popen([*shlex.split(DOCKER_COMPOSE), *shlex.split(cmd)], cwd=dirpath).wait()
    if code != 0:
        print('Execute command failed')
        exit(code)

def install(args):
    download_package(args.package)
    dirpath = get_package_path(args.package)
    execute_docker_compose(dirpath, 'up -d')
    print('Package {} install complete'.format(args.package))

def uninstall(args):
    dirpath = get_package_path(args.package)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        download_package()
    execute_docker_compose(dirpath, 'down')
    shutil.rmtree(dirpath)
    print('Package {} uninstall complete'.format(args.package))

def update(args):
    uninstall(args)
    install(args)
    print('Package {} update complete'.format(args.package))

def set_docker_compose(version):
    global DOCKER_COMPOSE
    DOCKER_COMPOSE = DC_DOCKER_COMPOSE or 'docker{}compose'.format('-' if int(version) == 1 else ' ')

def format_env():
    set_docker_compose(1)
    return textwrap.dedent(f'''
    environments:
      {'DC_HOST':<21} {DC_HOST}
      {'DC_PACKAGE_PATH':<21} {DC_PACKAGE_PATH}
      {'DC_DOCKER_COMPOSE':<21} {DC_DOCKER_COMPOSE}
    ''')

def format_global():
    return textwrap.dedent(f'''
    global constants:
      {'HOST':<21} {HOST}
      {'HOME':<21} {HOME}
      {'PACKAGE_PATH':<21} {PACKAGE_PATH}
      {'DOCKER_COMPOSE':<21} {DOCKER_COMPOSE}
    ''')

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=format_env()+format_global())
    
    subparsers = parser.add_subparsers()
    install_parser = subparsers.add_parser('install')
    install_parser.set_defaults(func=install)
    uninstall_parser = subparsers.add_parser('uninstall')
    uninstall_parser.set_defaults(func=uninstall)
    update_parser = subparsers.add_parser('update')
    update_parser.set_defaults(func=update)

    parser.add_argument('--version', default='1', choices=['1', '2'], help='Docker compose version')
    install_parser.add_argument('package')
    uninstall_parser.add_argument('package')
    update_parser.add_argument('package')

    args = parser.parse_args()
    set_docker_compose(args.version)

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_usage()
        # print(format_env())


if __name__ == '__main__':
    main()
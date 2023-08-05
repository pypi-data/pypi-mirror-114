import os
from argparse import ArgumentError
from string import Template

import yaml


class Docker(object):
    @staticmethod
    def _get_main_docker_compose_service():
        for name, info in Docker._gel_all_docker_compose_services().items():
            if 'build' in info:
                return name

    @staticmethod
    def _gel_all_docker_compose_services():
        if os.path.exists('docker-compose.yml'):
            with open('docker-compose.yml') as file:
                return yaml.load(file, Loader=yaml.FullLoader)['services']
        return {}

    @staticmethod
    def command_interceptor(command, *remainders, service=None, **_):
        if service is None:
            remainders = list(remainders)
            if remainders and eval(remainders[0]) in Docker._gel_all_docker_compose_services():
                service = eval(remainders[0])
                remainders.pop(0)
            else:
                service = Docker._get_main_docker_compose_service()
        elif service not in Docker._gel_all_docker_compose_services():
            raise ArgumentError(service, 'No such service: "%s"' % service)

        return Template(command).safe_substitute(service=service), tuple(remainders)

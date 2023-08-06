import logging
import re
from argparse import ArgumentParser, Namespace
from importlib import import_module
from os import makedirs
from os.path import abspath, exists, join

from zope.interface import implementer

from cpcli.commands import ICommand
from cpcli.runner import Runner
from cpcli.utils.cmdtypes import readable_dir
from cpcli.utils.constants import CONFIG_FILE_NAME

logger = logging.getLogger()


@implementer(ICommand)
class InitCommand:
    def add_options(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            'ProjectName',
            action='store',
            type=str,
            help=(
                "Name of the `cpcli` project where all the files are stored."
                " In case, you want to keep your current directory"
                " as project root - Specify the name as \'.\'"
            )
        )
        parser.add_argument(
            '-p', '--project-path',
            action='store',
            type=readable_dir,
            required=False,
            help=(
                'Path to the project directory, if not specified it is taken as'
                ' ./<project-name>'
            )
        )

    @staticmethod
    def _is_valid_project_name(project_name):
        def _module_exists(module_name):
            try:
                import_module(module_name)
                return True
            except ImportError:
                return False

        if not re.search(r'^[_a-zA-Z]\w*$', project_name):
            logger.error(
                'Project names must begin with a letter and contain '
                'only\nletters, numbers and underscores'
            )
        elif _module_exists(project_name):
            logger.error(f'Module {project_name} already exists')
        else:
            return True
        return False

    def run(self, args: Namespace, __: Runner) -> None:
        project_name = args.ProjectName
        project_dir = args.project_path or project_name

        if project_name == '.':
            project_dir = abspath('.')

        config_path = join(project_dir, CONFIG_FILE_NAME)

        if exists(config_path):
            logger.error(f'{CONFIG_FILE_NAME} already exists in {project_dir}')
            return

        if project_name != '.' and not self._is_valid_project_name(project_name):
            return

        if not exists(project_dir):
            makedirs(project_dir)
            logger.debug(f'Created project directory: {project_name}')

        with open(config_path, 'w') as file:
            file.write('')
            logger.debug(f'Created config file {CONFIG_FILE_NAME}')

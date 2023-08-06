import inspect
import os
from argparse import ArgumentParser, ArgumentError, Namespace
from contextlib import suppress
from typing import Dict, Optional

from zope.interface import Interface, implementer
from zope.interface.exceptions import Invalid, MultipleInvalid
from zope.interface.verify import verifyClass

import cpcli
from cpcli.runner import Runner
from cpcli.utils.cmdtypes import readable_file, valid_uri
from cpcli.utils.config import CpCliConfig
from cpcli.utils.constants import CONTEST_URI_HELP
from cpcli.utils.misc import walk_modules


class ICommand(Interface):
    def add_options(parser: ArgumentParser) -> None:
        pass

    def run(args: Namespace, runner: Runner) -> None:
        pass


def iter_subcommands(cls):
    for module in walk_modules('cpcli.commands'):
        for obj in vars(module).values():
            with suppress(Invalid, MultipleInvalid):
                if (
                        inspect.isclass(obj)
                        and verifyClass(ICommand, obj)
                        and obj.__module__ == module.__name__
                        and not obj == cls
                ):
                    yield obj


@implementer(ICommand)
class BaseCommand:

    def __init__(self):
        self.subcommands: Dict[str, BaseCommand] = {}
        for cmd in iter_subcommands(BaseCommand):
            cmdname = cmd.__module__.split('.')[-1]
            self.subcommands[cmdname] = cmd()

        self.config = CpCliConfig()

    @property
    def templates_dir(self) -> str:
        return os.path.join(cpcli.__path__[0], 'templates')  # type: ignore  # mypy issue #1422

    @classmethod
    def from_parser(cls, parser: ArgumentParser):
        obj = cls()
        obj.add_options(parser)
        return obj

    def add_options(self, parser: ArgumentParser) -> None:
        """Adds new sub-commands/flags/options to the parser"""
        parser.add_argument(
            '-t', '--template',
            action='store',
            type=readable_file,
            default=os.path.join(self.templates_dir, 'Template.cpp'),
            required=False,
            help='Competitive programming template file',
        )

        parser.add_argument(
            '-c', '--contest-uri',
            action='store',
            type=valid_uri,
            required=False,
            help=CONTEST_URI_HELP
        )

        # Update all the subparsers
        sub_parsers = parser.add_subparsers(dest='command')
        for name, subcmd in self.subcommands.items():
            subcmd_parser = sub_parsers.add_parser(name)
            subcmd.add_options(subcmd_parser)

    def load_runner(self, args) -> Runner:
        if not args.contest_uri:
            raise ArgumentError(None, 'the following arguments are required: -c/--contest-uri')

        return Runner(
            uri=args.contest_uri,
            template=args.template,
            config=self.config
        )

    def run(self, args: Namespace, runner: Optional[Runner] = None) -> None:
        if args.command != 'init':
            runner = self.load_runner(args)

            # BaseCommand downloads the cache at the first load
            # We dont want to download questions again and again
            if args.command != 'download':
                runner.load_questions()

        if args.command:
            self.subcommands[args.command].run(args, runner)

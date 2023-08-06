import logging
from argparse import ArgumentParser, Namespace

from zope.interface import implementer

from cpcli.commands import ICommand
from cpcli.runner import Runner
from cpcli.utils.python import multiline_input

logger = logging.getLogger()


@implementer(ICommand)
class TestCaseCommand:
    def add_options(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            '-q', '--question',
            action='store',
            required=True,
            help='Substring representing Question Name or 1 based index'
        )
        testcase_group = parser.add_mutually_exclusive_group()
        testcase_group.add_argument(
            '-a', '--add',
            action='store_true',
            required=False,
            default=False,
            help='Add a new custom test case'
        )
        testcase_group.add_argument(
            '-d', '--delete',
            action='store',
            required=False,
            help='Add a new custom test case'
        )

    def run(self, args: Namespace, runner: Runner) -> None:
        question = runner.get_question(args.question)

        if not question:
            logger.warning('Invalid question entered. Following are available:')
            runner.show_all_questions()
        else:
            logger.info(f'Selected: {question.title}')
            if args.add:
                logger.info('Enter Sample Input:  (leave empty line to submit)')
                sample_input = multiline_input()
                logger.info('Enter Sample Output:  (leave empty line to submit)')
                sample_output = multiline_input()

                question.add_test(sample_input, sample_output, custom_testcase=True)
                runner.save_questions()
            elif args.delete:
                test = question.remove_test(args.delete)
                if test is not None:
                    logger.info(f'Deleted {test}')
                    runner.save_questions()
                else:
                    logger.error(f'No valid test with idx={args.delete} found ❗')
            else:
                logger.error('No option chosen ❗')

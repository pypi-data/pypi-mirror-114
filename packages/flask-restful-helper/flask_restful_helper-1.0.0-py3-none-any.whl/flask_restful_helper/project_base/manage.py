"""
開發環境CLI
"""
import click
import os
import unittest
from tests.roles.administrator_test import AdministratorTests
from main import create_app

app = create_app(os.getenv('config_type', 'dev'))


@click.group()
def cli():
    """
    預設CLI
    """


@cli.command()
def dev():
    """
    執行開發環境
    """

    app.run(port=5000)


@cli.command()
def test():
    # region For 單一測試
    # single_test = unittest.TestSuite()
    # single_test.addTest(AdministratorTests('test_list_all_absence_category_return_200_or_204'))
    # unittest.TextTestRunner(verbosity=2).run(single_test)
    # endregion

    tests = unittest.TestLoader().discover(os.path.join('tests', 'roles'), pattern='*_test.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    # 為了讓runner知道成功或失敗
    return exit(1) if result.errors else exit(0)


if __name__ == '__main__':
    cli()

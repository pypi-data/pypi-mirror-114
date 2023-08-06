import shutil
from pathlib import Path

import click

from flask_restful_helper.flask_admin_utils import read_template, write2file, \
    copy_config, copy_and_overwrite, build_prompt


@click.group()
def cli():
    pass


@cli.command('startproject')
@click.option('-f', '--force', 'force', help='強制重開專案', default=False)
def start_project(force):
    prompt_args = build_prompt()
    project_base_dir = Path(__file__).parent.joinpath('project_base')
    test_base_dir = Path(__file__).parent.joinpath('test_base')
    working_dir = Path()
    if not force and working_dir.joinpath('main').exists():
        print('main 已經存在， 如果依然要執行初始化請加入參數 --force')
        return

    if force:
        shutil.rmtree(working_dir.joinpath('main'))
        shutil.rmtree(working_dir.joinpath('tests'))
        working_dir.joinpath('manage.py').unlink()

    copy_and_overwrite(project_base_dir.joinpath('main'), working_dir.joinpath('main'), tree=True)
    copy_and_overwrite(test_base_dir.joinpath('tests'), working_dir.joinpath('tests'), tree=True)
    working_dir.joinpath('tests', 'functions', 'db', 'sqls').mkdir(parents=True, exist_ok=True)
    shutil.copy(project_base_dir.joinpath('manage.py'), working_dir.joinpath('manage.py'))
    shutil.copy(project_base_dir.joinpath('wsgi.py'), working_dir.joinpath('wsgi.py'))

    copy_config(project_base_dir, working_dir, prompt_args)
    print('執行開發伺服器 : python manage.py dev')


@cli.command('startaccountapp')
def start_account_app():
    app_name = 'account'
    account_path = Path(__file__).parent.joinpath('app_base', app_name)
    apps_path = Path().joinpath('apps', app_name)
    shutil.copytree(account_path, apps_path)

    print('請手動將路由註冊進 main/router.py')


@cli.command('startapp')
def start_app():
    project_base_path = Path(__file__).parent.joinpath('app_base', 'clean')
    while True:
        app_name = input('輸入 App 名稱：')
        if app_name[0].isnumeric():
            print('請勿以數字開頭')
            continue
        break

    apps_path = Path().joinpath('apps')
    print(f'creating {apps_path}')
    apps_path.joinpath(app_name).mkdir(parents=True, exist_ok=True)
    app_path = apps_path.joinpath(app_name)
    for category in ['api_view', 'logic', 'manager', 'model', 'schema']:
        print(f'creating {category}')
        py_string = read_template(project_base_path.joinpath(f'{category}s', f'{category}.template'), app_name=app_name)
        app_path.joinpath(f'{category}s').mkdir(exist_ok=True)
        write2file(app_path.joinpath(f'{category}s', f'{category}.py'), py_string)

    for category in ['router']:
        print(f'creating {category}')
        py_string = read_template(project_base_path.joinpath(f'{category}.template'), app_name=app_name)
        write2file(app_path.joinpath(f'{category}.py'), py_string)
    shutil.copy(project_base_path.joinpath('__init__.py'), app_path.joinpath('__init__.py'))


if __name__ == '__main__':
    cli()

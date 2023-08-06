import random
import shutil
import string
from pathlib import Path
from string import Template


def build_prompt():
    allow_dbs = ['mysql', 'sqlite']
    db_type = ''
    db_ip = ''
    db_username = ''
    db_password = ''
    db_port = ''
    db_database = ''
    while True:
        db_type = input('DB TYPE:  mysql | sqlite ：')

        if db_type not in allow_dbs:
            continue
        if db_type == 'sqlite':
            break
        else:
            db_ip = input("MYSQL IP：")
            db_username = input("MYSQL USERNAME：")
            db_password = input("MYSQL PASSWORD：")
            db_port = input("MYSQL PORT：")
            db_database = input("MYSQL DATABASE：")
            break

    prompt = {'db_type': db_type,
              'db_ip': db_ip,
              'db_username': db_username,
              'db_password': db_password,
              'db_port': db_port,
              'db_database': db_database}
    return prompt


def read_template(filename, **kwargs):
    """讀入template"""
    with open(filename, 'r', encoding='utf-8') as f:
        template = Template(f.read())
        return template.substitute(**kwargs)


def write2file(path, py_string):
    """寫入py"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(py_string)


def _build_database_string(database_type, **kwargs):
    if database_type == 'mysql':
        database_string = f"mysql+pymysql://{kwargs.get('db_username')}:{kwargs.get('db_password')}@{kwargs.get('db_ip')}:{kwargs.get('db_port')}/{kwargs.get('db_database')}"
        return database_string
    elif database_type == 'sqlite':
        database_string = 'sqlite:///sqlite.db'
        return database_string


def copy_config(project_base_dir, working_dir, prompt_args):
    if prompt_args.get('db_type') == 'mysql':
        database_string = _build_database_string(prompt_args.get('db_type'),
                                                 db_ip=prompt_args.get('db_ip'),
                                                 db_username=prompt_args.get('db_username'),
                                                 db_password=prompt_args.get('db_password'),
                                                 db_port=prompt_args.get('db_port'),
                                                 db_database=prompt_args.get('db_database'))
    elif prompt_args.get('db_type') == 'sqlite':
        database_string = _build_database_string(prompt_args.get('db_type'))
    else:
        raise ValueError('db_type 錯誤')
    working_dir.joinpath('config').mkdir(parents=True, exist_ok=True)
    yaml_string = read_template(project_base_dir.joinpath('config', 'dev.template'),
                                database_string=database_string, jwt_secret_key=generate_random_string(30))
    write2file(working_dir.joinpath('config', 'dev.yaml'), yaml_string)


def generate_random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


def copy_and_overwrite(src: Path, dst: Path, tree=False):
    if tree:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

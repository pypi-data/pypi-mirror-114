import json
from flask_testing import TestCase
from app import create_app
from tests.functions.db.db_common import DbCommon
import os


class TestBase(TestCase):
    username = None
    password = None
    login_url = ''  # 請填寫登入api url

    def create_app(self):
        return create_app(os.getenv('config_type', 'dev'))

    def setUp(self):
        db_common = DbCommon()
        if self.app.config['IS_NEED_INIT_DB_EVERY_TEST']:
            db_common.init_db_data(db_conn_host=self.app.config['DB_CONN_HOST'],
                                   db_conn_port=self.app.config['DB_CONN_PORT'],
                                   db_conn_user=self.app.config['DB_CONN_USER'],
                                   db_conn_password=self.app.config['DB_CONN_PASSWORD'],
                                   db_conn_db=self.app.config['DB_CONN_DB'])
        self.username = self.app.config[f'{self.role}_USERNAME']
        self.password = self.app.config[f'{self.role}_PASSWORD']
        self.login(self.username, self.password)

    def login(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        with self.app.test_client() as client:
            res = client.post(self.login_url, data=json.dumps(data),
                              headers={"Content-Type": "application/json"})

        self.access_token = res.json['data']['access_token']
        self.user = res.json['data']['user_data']
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.access_token}'}

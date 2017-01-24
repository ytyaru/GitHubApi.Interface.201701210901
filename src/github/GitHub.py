#!python3
#encoding:utf-8
from github.api import RequestParam
from github.api.repositories import Repositories
class GitHub:
    def __init__(self, db_path_account, db_path_api, username):
        self.req = RequestParam.RequestParam(db_path_account, db_path_api, username)
        self.repo = Repositories.Repositories(self.req)

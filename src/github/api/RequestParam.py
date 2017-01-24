#!python3
#encoding:utf-8
import os.path
import dataset
class RequestParam:
    def __init__(self, db_path_account, db_path_api, username):
        self.auth_param = RequestParam.AuthParam(db_path_account, db_path_api, username)

    def get(self, http_method, endpoint):
        params = self.auth_param.get(http_method, endpoint)
        if not("headers" in params.keys()):
            params['headers'] = {}
        params['headers'].update({"Time-Zone": "Asia/Tokyo"})
        if not("Accept" in params['headers'].keys()):
            params['headers'].update({"Accept": "application/vnd.github.v3+json"})
        return params

    from tkinter import Tk
    class AuthParam:
        def __init__(self, db_path_account, db_path_api, username):
            self.username = username
            self.db_account = dataset.connect('sqlite:///' + db_path_account)
            self.db_api = dataset.connect('sqlite:///' + db_path_api)

        def get(self, http_method, endpoint):
            params = {}
            account = self.db_account['Accounts'].find_one(Username=self.username)
            api = self.db_api['Apis'].find_one(HttpMethod=http_method, Endpoint=endpoint)
            if ("Token" in api['AuthMethods']):
                token = self.__get_access_token(account['Id'], api['Grants'].split(","))
                params['headers'] = {"Authorization": "token " + token}
            elif ("ClientId" in api['AuthMethods']):
                raise Exception('Not implemented clientId authorization.')
            elif ("Basic" in api['AuthMethods']):
                params['auth'] = (self.username, account['Password'])
                two_factor = self.db_account['TwoFactors'].find(AccountId=account['Id'])
                if not(None is two_factor):
                    t = Tk()
                    otp = t.clipboard_get()
                    t.destroy()
                    params['headers'] = {"X-GitHub-OTP": otp}
            else:
                raise Exception('Not found AuthMethods: {0} {1}'.format(api['HttpMethod'], api['Endpoint']))
            return params

        def __get_access_token(self, account_id, scopes):
            sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(account_id)
            if (0 < len(scopes)):
                sql = sql + " AND ("
                for s in scopes:
                    sql = sql + "(',' || Scopes || ',') LIKE '%,{0},%'".format(s) + " OR "
                sql = sql.rstrip(" OR ")
                sql = sql + ')'
            tokens = self.db_account.query(sql)
            token = None
            for t in tokens:
               token = t['AccessToken']
            return token

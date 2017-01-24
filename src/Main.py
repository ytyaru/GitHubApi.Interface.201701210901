from github import GitHub

username = "github_username"
db_path_account = "C:/GitHub.Accounts.sqlite3"
db_path_api = "C:/GitHub.Apis.sqlite3"

g = GitHub.GitHub(db_path_account, db_path_api, username)
g.repo.create('repository_name', description='this is repository description.', homepage='http://homepage.com')

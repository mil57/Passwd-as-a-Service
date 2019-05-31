from flask import Flask
from flask import request
from service import *
import json

app = Flask(__name__)


# Index, and test method
@app.route("/")
def index():
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Config file is missing or malformed!", 500

    return "Service Online"


# Route that return list of all users
@app.route('/users')
def users():
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Config file is missing or malformed!", 500

    # Load the users from passd
    users = load_passwd(pass_path)

    # Return the result
    return json.dumps(users)


# Route that return list of all users
@app.route('/users/query')
def users_query():
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Config file is missing or malformed!", 500

    # Load the users from passd
    users = load_passwd(pass_path)

    # Search the users
    q = request.args
    result = search_users(users, name=q.get("name"), uid=q.get("uid"), comment=q.get("comment"), home=q.get("home"),
                          shell=q.get("shell"), gid=q.get("gid"))

    # Return result if there are any
    return json.dumps(result)


# Route that return list of all users
@app.route('/users/<int:uid>')
def users_uid(uid):
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Config file is missing or malformed!", 500

    # Load the users from passd
    users = load_passwd(pass_path)

    # Search the users
    result = search_users(users, uid=uid)

    # Return result if there are any
    if len(result) > 0:
        return json.dumps(result[0])
    else:
        return "User not Found", 404

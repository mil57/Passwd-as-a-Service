from flask import Flask
from flask import request
from service import *
import json

# Initialize the app
app = Flask(__name__)


# Index, and test method
@app.route("/")
def route_index():
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Internal Server Error", 500

    return "Service Online"


# Route that return list of all users
@app.route('/users')
def route_users():
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Internal Server Error", 500

    # Load the users from passd
    users = load_passwd(pass_path)
    if users is None:
        return "Internal Server Error", 500

    # Return the result
    return json.dumps(users)


# Route that return list of all users that match the query
@app.route('/users/query')
def route_users_query():
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Internal Server Error", 500

    # Load the users from passd
    users = load_passwd(pass_path)
    if users is None:
        return "Internal Server Error", 500

    # Search the users
    q = request.args
    result = search_users(users, name=q.get("name"), uid=q.get("uid"), comment=q.get("comment"), home=q.get("home"),
                          shell=q.get("shell"), gid=q.get("gid"))

    # Return result if there are any
    return json.dumps(result)


# Route that return user with this uid
@app.route('/users/<int:uid>')
def route_users_uid(uid):
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Internal Server Error", 500

    # Load the users from passd
    users = load_passwd(pass_path)
    if users is None:
        return "Internal Server Error", 500

    # Search the users
    result = search_users(users, uid=uid)

    # Return result if there are any
    if len(result) > 0:
        return json.dumps(result[0])
    else:
        return "User not Found", 404


# Route that return user with this uid
@app.route('/users/<int:uid>/groups')
def route_users_groups(uid):
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Internal Server Error", 500

    # Load the users from passd
    users = load_passwd(pass_path)
    if users is None:
        return "Internal Server Error", 500

    # Load the groups from group file
    groups = load_group(group_path)
    if groups is None:
        return "Internal Server Error", 500

    # Search the users
    result = search_users(users, uid=uid)

    # Return result if there are any
    if len(result) > 0:
        name = [result[0]["name"]]
        return json.dumps(search_groups(groups, members=name))
    else:
        return "User not Found", 404


# Route that return list of all groups
@app.route('/groups')
def route_groups():
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Internal Server Error", 500

    # Load the groups from group file
    groups = load_group(group_path)
    if groups is None:
        return "Internal Server Error", 500

    # Return the result
    return json.dumps(groups)


# Route that return list of all groups that match the query
@app.route('/groups/query')
def route_groups_query():
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Internal Server Error", 500

    # Load the users from passd
    groups = load_group(group_path)
    if groups is None:
        return "Internal Server Error", 500

    # Search the users
    q = request.args
    result = search_groups(groups, name=q.get("name"), gid=q.get("gid"), members=q.getlist('member'))

    # Return result if there are any
    return json.dumps(result)


# Route that return group with this gid
@app.route('/groups/<int:gid>')
def route_groups_gid(gid):
    # Check the config file to load the paths to the passwd/group files
    pass_path, group_path = load_paths()

    # Return Error if file paths is not found
    if pass_path is None:
        return "Internal Server Error", 500

    # Load the users from passd
    groups = load_group(group_path)
    if groups is None:
        return "Internal Server Error", 500

    # Search the users
    result = search_groups(groups, gid=gid)

    # Return result if there are any
    if len(result) > 0:
        return json.dumps(result[0])
    else:
        return "Group not Found", 404

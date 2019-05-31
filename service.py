# Define constants for parsing user and group information
NAME = 0
UID = 2
GID = 3
COMMENT = 4
HOME = 5
SHELL = 6
GROUP_GID = 2
MEMBERS = 3


# Methods needed to load and parse information from passwd and group file

# This method Load the paths of the target files from config file and return them as (pass_path, group_path)
# If return (None, None), the config file is missing or malformed
def load_paths():
    try:
        with open("config.txt", "r") as config:
            # Read the paths
            pass_path = config.readline()
            group_path = config.readline()

            # Remove the newline character
            pass_path = pass_path.replace("\n", "")
            group_path = group_path.replace("\n", "")
    except IOError:
        # Error message
        print("Config file is missing or malformed! See README for example of config.txt")
        pass_path = group_path = None
    finally:
        config.close()

    return pass_path, group_path


# This method take in the path of passwd file and return a object containing info of all users
def load_passwd(pass_path):
    # Load the list pf user string from passwd file
    with open(pass_path, "r") as passwd_file:
        raw_users = passwd_file.readlines()

    # Go through the list of user string and parse them into a object
    users = []
    for raw_user in raw_users:
        # process the string and split it by :
        info = raw_user.replace("\n", "").split(":")
        # UID and GID need to be convert to int
        users.append({"name": info[NAME], "uid": int(info[UID]), "gid": int(info[GID]), "comment": info[COMMENT],
                      "home": info[HOME], "shell": info[SHELL]})

    return users


# This method take in the path of group file and return a object containing info of all groups
def load_group(group_path):
    # Load the list pf user string from passwd file
    with open(group_path, "r") as group_file:
        raw_groups = group_file.readlines()

    # Go through the list of user string and parse them into a object
    groups = []
    for raw_group in raw_groups:
        # process the string and split it by :
        info = raw_group.replace("\n", "").split(":")
        # GID need to be convert to int
        group = {"name": info[NAME], "gid": int(info[GROUP_GID]), "members": []}

        # Form the group member list
        if len(info[MEMBERS]) > 0:
            for member in info[MEMBERS].split(","):
                group["members"].append(member)

        groups.append(group)

    return groups


# This method take in the users object and optional parameters, and return a list of matching users
# If a parameter is not given, it is not checked
# If a argument is given, the result must match that argument
def search_users(users, name=None, uid=None, gid=None, comment=None, home=None, shell=None):
    # Make sure at least one parameter is given
    if name is not None or uid is not None or gid is not None or comment is not None or home is not None or \
            shell is not None:
        pass
    else:
        return None

    # Go through the list of user and check if they match
    result = []
    for user in users:
        if name is not None and user["name"] != name:
            continue
        if uid is not None and user["uid"] != int(uid):
            continue
        if gid is not None and user["gid"] != int(gid):
            continue
        if comment is not None and user["comment"] != comment:
            continue
        if home is not None and user["home"] != home:
            continue
        if shell is not None and user["shell"] != shell:
            continue
        # Append to result if this user match all given parameter
        result.append(user)

    return result


# A helper method that determind of query members are subset of group members
def compare_members(group_members, query_members):
    for member in query_members:
        if member in group_members:
            continue
        else:
            return False
    return True


# This method take in the groups object and optional parameters, and return a list of matching groups
# If a parameter is not given, it is not checked
# If a non-member argument is given, the result must match that argument
# If a list of member is given, it must be a subset of members of the matching group
def search_groups(groups, name=None, gid=None, members=None):
    # Make sure at least one parameter is given
    if name is not None or members is not None or gid is not None:
        pass
    else:
        return None

    # Go through the list of user and check if they match
    result = []
    for group in groups:
        if name is not None and group["name"] != name:
            continue
        if gid is not None and group["gid"] != int(gid):
            continue
        if members is not None and compare_members(group["members"], members) is False:
            continue

        # Append to result if this user match all given parameter
        result.append(group)

    return result
'''
pass_path, group_path = load_paths()

users = load_passwd(pass_path)
groups = load_group(group_path)
list1 = search_groups(groups, gid=21, members=["azureuser"])

print(list1)
'''


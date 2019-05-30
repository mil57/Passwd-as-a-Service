
# Load the paths of the target files, remove the newline character
with open("config.txt", "r") as config:
    pass_path = config.readline()
    pass_path = pass_path.replace("\n", "")
    group_path = config.readline()
    group_path = group_path.replace("\n", "")

with open(pass_path, "r") as passwd_file:
    print(passwd_file.readline())

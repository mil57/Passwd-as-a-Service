import unittest
from  service import *

# Test Paths
PASS_PATH = "./test/passwd"
GROUP_PATH = "./test/group"

# Test Results
TEST_USERS = [{'name': 'root', 'uid': 0, 'gid': 0, 'comment': 'root', 'home': '/root', 'shell': '/bin/bash'},
              {'name': 'daemon', 'uid': 1, 'gid': 1, 'comment': 'daemon', 'home': '/usr/sbin',
               'shell': '/usr/sbin/nologin'},
              {'name': 'bin', 'uid': 2, 'gid': 2, 'comment': 'bin', 'home': '/bin', 'shell': '/usr/sbin/nologin'},
              {'name': 'sys', 'uid': 3, 'gid': 3, 'comment': 'sys', 'home': '/dev', 'shell': '/usr/sbin/nologin'},
              {'name': 'sync', 'uid': 4, 'gid': 65534, 'comment': 'sync', 'home': '/bin', 'shell': '/bin/sync'},
              {'name': 'syslog', 'uid': 5, 'gid': 60, 'comment': 'games', 'home': '/usr/games',
               'shell': '/usr/sbin/nologin'},
              {'name': 'azureuser', 'uid': 6, 'gid': 12, 'comment': 'man', 'home': '/var/cache/man',
               'shell': '/usr/sbin/nologin'}]
TEST_USERS_UID = {'name': 'root', 'uid': 0, 'gid': 0, 'comment': 'root', 'home': '/root', 'shell': '/bin/bash'}
TEST_GROUPS = [{'name': 'root', 'gid': 0, 'members': []}, {'name': 'adm', 'gid': 4, 'members': ['syslog', 'azureuser']},
               {'name': 'dialout', 'gid': 20, 'members': ['azureuser']},
               {'name': 'sudo', 'gid': 27, 'members': ['azureuser']},
               {'name': 'audio', 'gid': 29, 'members': ['pulse', 'azureuser']},
               {'name': 'dip', 'gid': 30, 'members': ['azureuser']}]
TEST_GROUPS_QUERY = [{'name': 'adm', 'gid': 4, 'members': ['syslog', 'azureuser']}]
TEST_USER_GROUPS = [{'name': 'adm', 'gid': 4, 'members': ['syslog', 'azureuser']},
               {'name': 'dialout', 'gid': 20, 'members': ['azureuser']},
               {'name': 'sudo', 'gid': 27, 'members': ['azureuser']},
               {'name': 'audio', 'gid': 29, 'members': ['pulse', 'azureuser']},
               {'name': 'dip', 'gid': 30, 'members': ['azureuser']}]

class PasswdAndGroupTestCase(unittest.TestCase):

    # Test loading users
    def test_users(self):
        users = load_passwd(PASS_PATH)
        self.assertEqual(users, TEST_USERS)

    # Test user search by uid
    def test_users_uid(self):
        users = load_passwd(PASS_PATH)
        user = search_users(users,uid=0)
        self.assertEqual(user[0], TEST_USERS_UID)

    # Test user search by query
    def test_users_query(self):
        users = load_passwd(PASS_PATH)
        user = search_users(users, home="/root")
        self.assertEqual(user[0], TEST_USERS_UID)

    # Test loading groups
    def test_groups(self):
        groups = load_group(GROUP_PATH)
        self.assertEqual(groups, TEST_GROUPS)

    # Test group search query
    def test_group_query(self):
        groups = load_group(GROUP_PATH)
        result = search_groups(groups, gid=4)
        self.assertEqual(result, TEST_GROUPS_QUERY)

    # Test user's groups
    def test_user_groups(self):
        users = load_passwd(PASS_PATH)
        user = search_users(users, name="azureuser")
        groups = load_group(GROUP_PATH)
        result = search_groups(groups, members=[user[0]["name"]])
        self.assertEqual(result, TEST_USER_GROUPS)



if __name__ == '__main__':
    unittest.main()

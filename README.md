# Passwd-as-a-Service
This is a coding challenge with potential security risks, not meant to be used in real life.

Passwd-as-a-Service is a HTTP service that exposes the user and group information on a UNIX-like system that is usually locked away in the UNIX /etc/passwd and /etc/group files.

### GET /users

Return a list of all users on the system, as defined in the /etc/passwd file.

Example Response:

[
{“name”: “root”, “uid”: 0, “gid”: 0, “comment”: “root”, “home”: “/root”,
“shell”: “/bin/bash”},
{“name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, “home”:
“/home/dwoodlins”, “shell”: “/bin/false”}
]

### GET /users/query[?name=\<nq>][&uid=\<uq>][&gid=\<gq>][&comment=\<cq>][&home=\<hq>][&shell=\<sq>]

Return a list of users matching all of the specified query fields. The bracket notation indicates that any of the
following query parameters may be supplied:
- name
- uid
- gid
- comment
- home
- shell

Only exact matches need to be supported.

Example Query: GET /users/query?shell=%2Fbin%2Ffalse

Example Response:

[
{“name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, “home”:
“/home/dwoodlins”, “shell”: “/bin/false”}
]

### GET /users/\<uid>

Return a single user with <uid>. Return 404 if <uid> is not found.

Example Response:

{“name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, “home”:
“/home/dwoodlins”, “shell”: “/bin/false”}

### GET /users/\<uid>/groups

Return all the groups for a given user.

Example Response:

[
{“name”: “docker”, “gid”: 1002, “members”: [“dwoodlins”]}
]

### GET /groups

Return a list of all groups on the system, a defined by /etc/group.

Example Response:

[
{“name”: “_analyticsusers”, “gid”: 250, “members”:
[“_analyticsd’,”_networkd”,”_timed”]},
{“name”: “docker”, “gid”: 1002, “members”: []}
]

### GET /groups/query[?name=<nq>][&gid=\<gq>][&member=\<mq1>[&member=\<mq2>][&...]]

Return a list of groups matching all of the specified query fields. The bracket notation indicates that any of the
following query parameters may be supplied:
- name
- gid
- member (repeated)

Any group containing all the specified members should be returned, i.e. when query members are a subset of
group members.

Example Query: GET /groups/query?member=_analyticsd&member=_networkd

Example Response:

[
{“name”: “_analyticsusers”, “gid”: 250, “members”:
[“_analyticsd’,”_networkd”,”_timed”]}
]

### GET /groups/\<gid>

Return a single group with <gid>. Return 404 if <gid> is not found.

Example Response:

{“name”: “docker”, “gid”: 1002, “members”: [“dwoodlins”]}

# File Structure
### app.py
Contain the web app framework code and http routes

### service.py
Contain functions for accessing, parsing, and searching the passwd/group files

### config.txt
This file specifies the location of the passwd file and the group file

Example:

```
/etc/passwd
/etc/group
```

### test.py
This file contain unit test for methods in service.py, to run the tests, use
```
python -m unittest test
```
### /test
This folder contains test files needed for the unit test

### requirements.txt
Contain Python packages needed to run this app

# How to run

## Prerequisite
Make sure you have Python 3 and PIP working

## Set up
1. Download the codes or clone the repo to your machine
2. In the directory, run this command to install the packages needed
```
pip install -r requirements.txt
```
3. Make sure the paths in config.txt is pointing to the passwd and group file in your system
The first line is for passwd, and the second line is for group

## Run
### For local testing, run 
```
flask run
``` 

use http://localhost:5000 on local browser to access the service
### For production 
```
flask run --host=0.0.0.0 --port=$PORT
``` 

$PORT should be replace with a port number meant for hosting web service



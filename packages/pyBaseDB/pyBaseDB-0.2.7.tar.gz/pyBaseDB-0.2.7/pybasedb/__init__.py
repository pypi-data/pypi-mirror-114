import os
import os.path as path
import json

USER_PATH = path.expanduser('~')
CURRENT_DIRS = os.listdir(USER_PATH)

if '.pyBase' not in CURRENT_DIRS:
    os.mkdir(f"{USER_PATH}/.pyBase")
    os.mkdir(f"{USER_PATH}/.pyBase/Schemas")
    data = {}
    json.dump(open(data, f"{USER_PATH}/.pyBase/Schemas/schema.json",'w'),indent=4)
    os.mkdir(f"{USER_PATH}/.pyBase/DBs")
else:
    PYBASE_FOLDER = os.listdir(f"{USER_PATH}/.pyBase")
    if 'Schemas' not in PYBASE_FOLDER:
        os.mkdir(f"{USER_PATH}/.pyBase/Schemas")
        data = {}
        json.dump(open(data, f"{USER_PATH}/.pyBase/Schemas/schema.json",'w'),indent=4)
    if 'DBs' not in PYBASE_FOLDER:
        os.mkdir(f"{USER_PATH}/.pyBase/DBs")
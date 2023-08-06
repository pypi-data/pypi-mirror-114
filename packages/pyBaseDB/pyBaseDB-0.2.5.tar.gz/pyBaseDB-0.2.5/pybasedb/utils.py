from pybasedb.pyBase import pyBase, create_database_from_schema
from os import listdir, mkdir
import os.path as path
import json
from webbrowser import open as webopen
import inspect

class Utils:

    def __init__(self):
        self.database = None

        folders = listdir(path.expanduser('~'))
        if '.pyBase' not in folders:
            mkdir(f'{path.expanduser("~")}/.pyBase')
            mkdir(f'{path.expanduser("~")}/.pyBase/Schemas')
            mkdir(f'{path.expanduser("~")}/.pyBase/DBs')
        self.__config_path = pyBase.getConfigPath()
        self.__schema_path = f'{self.__config_path}/Schemas'
        self.__schema = json.load(open(f'{self.__schema_path}/schema.json','r'))

    def create_db_schema(self, name: str):
        current_dbs = self.__schema.keys()
        if name in current_dbs:
            print('DB exists in schema')
            return
        self.__schema[name] = {
            "columns": [],
            "views": [],
            "policies": {
                "READ": '*',
                "WRITE": '*',
                "DELETE": '*',
                "UPDATE": '*'
            }
        }
        self.database = name
        self.add_field('id','str',primary=True, allow_empty=False)
        return self
    
    def add_field(self, name:str, field_type:'str | int | bool | dict | list', primary:bool=False,allow_empty:bool=False, **kwargs):
        if not self.database:
            print('DB not set/created')
            return
        index = len(self.__schema[self.database]['columns'])
        block = {
            "index": index,
            "name": name,
            "api_name": name,
            "type": field_type,
            "optional": [{
                "primary": 'yes' if primary else 'no',
                "allow_empty": 'yes' if allow_empty else 'no'
            }]
        }
        for key in kwargs.keys():
            block['optional'][0][key] = kwargs[key]
        self.__schema[self.database]['columns'].append(block)
        return self
    
    def add_view(self, name:str, fields:list):
        if not self.database:
            print('DB not set/created')
            return
        v = [view['name'] for view in self.__schema[self.database]['views']]
        if name not in v:
            self.__schema[self.database]['views'].append({
                "name": name,
                "fields": fields
            })
        return self
    
    def set_db(self, name:str):
        if name not in self.__schema.keys():
            print('DB does not exist in schema')
            return
        self.database = name
        return self

    def save(self):
        if not self.database:
            print('DB not set/created')
            return
        self.add_view('default',[f['name'] for f in self.__schema[self.database]['columns']])
        json.dump(self.__schema,open(f'{self.__schema_path}/schema.json','w'), indent=4)
        create_database_from_schema(verbose=True)
        return self
    
    def open_docs(self):
        webopen(f"file://{inspect.getfile(pyBase).replace('pyBase.py','Docs\\index.html')}")

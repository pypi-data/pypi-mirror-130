__version__ = '999.999.999999'
import os
import json
import copy
from typing import Union
from io import TextIOWrapper
import yaml
import requests
import base64

print('WARNING!')
print("Pickle Rick has been renamed to 'rickled', see http://blog.zipfian.science/news/2021-12-06-pickle-rick-renamed.html for more")
print("You can install it:")
print("\tpip install rickled")
print("This package will be discontinued from 31-01-2022")

class BasicRick:
    """
        A base class that creates internal structures from embedded structures.

        Args:
            base (str): String (YAML or JSON, file path to YAML/JSON file), text IO stream, dict (default = None).
            deep (bool): Internalize dictionary structures in lists (default = False).

        Raises:
            ValueError: If the given base object can not be handled.
    """
    def _iternalize(self, dictionary : dict, deep : bool, **init_args):
        for k, v in dictionary.items():
            if isinstance(v, dict):
                self.__dict__.update({k:BasicRick(v, deep, **init_args)})
                continue
            if isinstance(v, list) and deep:
                new_list = list()
                for i in v:
                    if isinstance(i, dict):
                        new_list.append(BasicRick(i, deep, **init_args))
                    else:
                        new_list.append(i)
                self.__dict__.update({k: new_list})
                continue

            self.__dict__.update({k:v})

    def __init__(self, base : Union[dict,str,TextIOWrapper,list] = None, deep : bool = False, **init_args):
        print('WARNING!')
        print("Pickle Rick has been renamed to 'rickled', see http://blog.zipfian.science/news/2021-12-06-pickle-rick-renamed.html for more")
        print("You can install it:")
        print("\tpip install rickled")
        print("This package will be discontinued from 31-01-2022")
        stringed = ''
        if base is None:
            return
        if isinstance(base, dict):
            self._iternalize(base, deep, **init_args)
            return

        if isinstance(base, TextIOWrapper):
            stringed = base.read()
        elif isinstance(base, list):
            for file in base:
                with open(file, 'r') as f:
                    stringed = f'{stringed}\n{f.read()}'
        elif os.path.isfile(base):
            with open(base, 'r') as f:
                stringed = f.read()
        elif isinstance(base, str):
            stringed = base

        if not init_args is None:
            for k, v in init_args.items():
                _k = f'_|{k}|_'
                stringed = stringed.replace(_k,json.dumps(v))

        try:
            dict_data = yaml.safe_load(stringed)
            self._iternalize(dict_data, deep, **init_args)
            return
        except Exception as exc:
            print("Tried YAML: {}".format(exc))
        try:
            dict_data = json.loads(base)
            self._iternalize(dict_data, deep, **init_args)
            return
        except Exception as exc:
            print("Tried JSON: {}".format(exc))

        raise ValueError('Base object could not be internalized, type {} not handled'.format(type(base)))

    def __repr__(self):
        keys = self.__dict__
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys if not str(k).__contains__(self.__class__.__name__) and not str(k).endswith('__meta_info') )
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __str__(self):
        return self.to_yaml_string()

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __setitem__(self, key, item):
        self.__dict__.update( {key : item} )

    def __getitem__(self, key):
        return self.__dict__[key]

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        current_loop = 0
        if self.__n < len(self.__dict__):
            name = list(self.__dict__.keys())[self.__n]
            while (str(name).__contains__(self.__class__.__name__) or str(name).endswith('__n')) and (current_loop < 9):
                self.__n += 1
                current_loop += 1
                if self.__n < len(self.__dict__):
                    name = list(self.__dict__.keys())[self.__n]
                else:
                    raise StopIteration
            if self.__n < len(self.__dict__):
                obj = self.__dict__[list(self.__dict__.keys())[self.__n]]
                self.__n += 1
                return obj
            else:
                raise StopIteration
        else:
            raise StopIteration

    def _recursive_search(self, dictionary, key):
        if key in dictionary:
            return dictionary[key]
        for k, v in dictionary.items():
            if isinstance(v, BasicRick):
                try:
                    value = self._recursive_search(v.__dict__, key)
                    return value
                except StopIteration:
                    continue
            if isinstance(v, dict):
                try:
                    value = self._recursive_search(v, key)
                    return value
                except StopIteration:
                    continue
        raise StopIteration

    def items(self):
        """
        Iterate through all key value pairs.

        Yields:
            tuple: str, object.
        """
        for key in self.__dict__.keys():
            if str(key).__contains__(self.__class__.__name__) or str(key).endswith('__n'):
                continue
            yield key, self.__dict__[key]

    def get(self, key : str, default=None):
        """
        Employs a recursive search of structure and returns the first found key-value pair.

        Args:
            key (str): key string being searched.
            default (any): Return value if nothing is found.

        Returns:
            obj: value found, or None for nothing found.
        """
        try:
            value = self._recursive_search(self.__dict__, key)
            return value
        except StopIteration:
            return default

    def values(self):
        """
        Gets the higher level values of the current Rick object.

        Returns:
            list: of objects.
        """
        keys = list(self.__dict__.keys())
        objects = [self.__dict__[k] for k in keys if not str(k).__contains__(self.__class__.__name__) and not str(k).endswith('__n')]

        return objects

    def keys(self):
        """
        Gets the higher level keys of the current Rick object.

        Returns:
            list: of keys.
        """
        keys = list(self.__dict__.keys())
        keys = [k for k in keys if not str(k).__contains__(self.__class__.__name__) and not str(k).endswith('__n')]

        return keys

    def dict(self, serialised : bool = False):
        """
        Deconstructs the whole object into a Python dictionary.

        Args:
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.

        Returns:
            dict: of object.
        """
        d = dict()
        for key, value in self.__dict__.items():
            if str(key).__contains__(self.__class__.__name__) or str(key).endswith('__meta_info'):
                continue
            if isinstance(value, BasicRick) or isinstance(value, PickleRick):
                d[key] = value.dict(serialised=serialised)
            elif isinstance(value, list):
                new_list = list()
                for element in value:
                    if isinstance(element, BasicRick):
                        new_list.append(element.dict(serialised=serialised))
                    else:
                        new_list.append(element)
                d[key] = new_list
            else:
                d[key] = value
        return d

    def has(self, key : str, deep=False) -> bool:
        """
        Checks whether the key exists in the object.

        Args:
            key (str): key string being searched.
            deep (bool): whether to search deeply (default = False).

        Returns:
            bool: if found.
        """
        if key in self.__dict__:
            return True
        if deep:
            try:
                self._recursive_search(self.__dict__, key)
                return True
            except StopIteration:
                return False
        return False

    def to_yaml_file(self, file_path : str, serialised : bool = True):
        """
        Does a self dump to a YAML file.

        Args:
            file_path (str): File path.
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = True).

        Notes:
            Functions and lambdas are always given in serialised form.
        """
        self_as_dict = self.dict(serialised=serialised)
        with open(file_path, 'w', encoding='utf-8') as fs:
            yaml.safe_dump(self_as_dict, fs)

    def to_yaml_string(self, serialised : bool = True):
        """
        Dumps self to YAML string.

        Args:
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = True).

        Notes:
            Functions and lambdas are always given in serialised form.

        Returns:
            str: YAML representation.
        """
        self_as_dict = self.dict(serialised=serialised)
        return yaml.safe_dump(self_as_dict, None)

    def to_json_file(self, file_path: str, serialised : bool = True):
        """
        Does a self dump to a JSON file.

        Args:
            file_path (str): File path.
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = True).

        Notes:
            Functions and lambdas are always given in serialised form.
        """
        self_as_dict = self.dict(serialised=serialised)
        with open(file_path, 'w', encoding='utf-8') as fs:
            json.dump(self_as_dict, fs)

    def to_json_string(self, serialised : bool = True):
        """
        Dumps self to YAML string.

        Args:
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = True).

        Notes:
            Functions and lambdas are always given in serialised form.

        Returns:
            str: JSON representation.
        """
        self_as_dict = self.dict(serialised=serialised)
        return json.dumps(self_as_dict)

    def add_attr(self, name, value):
        """
        Add a new attribute member to Rick.

        Args:
            name (str): Property name.
            value (any): Value of new member.
        """
        self.__dict__.update({name: value})

class PickleRick(BasicRick):
    """
        An extended version of the BasicRick that can load OS environ variables and Python Lambda functions.

        Args:
            base (str, list): String (YAML or JSON, file path to YAML/JSON file) or list of file paths, text IO stream, dict.
            deep (bool): Internalize dictionary structures in lists.
            load_lambda (bool): Load lambda as code or strings.
    """

    def _iternalize(self, dictionary : dict, deep : bool, **init_args):
        for k, v in dictionary.items():
            if isinstance(v, dict):
                if 'type' in v.keys() and v['type'] == 'env':
                    self.add_env_variable(name=k,
                                          load=v['load'],
                                          default=v.get('default', None))
                    continue
                if 'type' in v.keys() and v['type'] == 'base64':
                    self.add_base64(name=k,
                                          load=v['load'])
                    continue
                if 'type' in v.keys() and v['type'] == 'from_file':
                    self.add_from_file(name=k,
                                       file_path=v['file_path'],
                                       load_as_rick=v.get('load_as_rick', False),
                                       deep=v.get('deep', False),
                                       load_lambda=v.get('load_lambda', False),
                                       is_binary=v.get('is_binary', False),
                                       encoding=v.get('encoding', 'utf-8'))
                    continue
                if 'type' in v.keys() and v['type'] == 'from_csv':
                    self.add_csv_file(name=k,
                                      file_path=v['file_path'],
                                      fieldnames=v.get('fieldnames', None),
                                      load_as_rick=v.get('load_as_rick', False),
                                      encoding=v.get('encoding', 'utf-8'))
                    continue
                if 'type' in v.keys() and v['type'] == 'api_json':
                    self.add_api_json_call(name=k,
                                           url=v['url'],
                                           http_verb=v.get('http_verb', 'GET'),
                                           headers=v.get('headers', None),
                                           params=v.get('params', None),
                                           body=v.get('body', None),
                                           load_lambda=v.get('load_lambda', False),
                                           deep=v.get('deep', False),
                                           expected_http_status=v.get('expected_http_status', 200))
                    continue
                if 'type' in v.keys() and v['type'] == 'html_page':
                    self.add_html_page(name=k,
                                       url=v['url'],
                                       headers=v.get('headers', None),
                                       params=v.get('params', None),
                                       expected_http_status=v.get('expected_http_status', 200))
                    continue
                if 'type' in v.keys() and v['type'] == 'lambda':
                    load = v['load']
                    imports = v.get('import', None)
                    if init_args and init_args['load_lambda']:
                        self.add_lambda(name=k,
                                        load=load,
                                        imports=imports)
                    else:
                        self.__dict__.update({k: v})
                    continue
                if 'type' in v.keys() and v['type'] == 'function':
                    name = v.get('name', k)
                    load = v['load']
                    args_dict = v.get('args', None)
                    imports = v.get('import', None)

                    if init_args and init_args['load_lambda']:
                        self.add_function(name=name,
                                          load=load,
                                          args=args_dict,
                                          imports=imports)
                    else:
                        self.__dict__.update({k: v})
                    continue
                self.__dict__.update({k:PickleRick(v, deep, **init_args)})
                continue
            if isinstance(v, list) and deep:
                new_list = list()
                for i in v:
                    if isinstance(i, dict):
                        new_list.append(PickleRick(i, deep, **init_args))
                    else:
                        new_list.append(i)
                self.__dict__.update({k: new_list})
                continue
            self.__dict__.update({k: v})

    def __init__(self, base: Union[dict,str,TextIOWrapper,list] = None, deep : bool = False, load_lambda : bool = False, **init_args):
        self.__meta_info = dict()
        init_args['load_lambda'] = load_lambda
        init_args['deep'] = deep
        self.__init_args = init_args
        super().__init__(base, **init_args)

    def dict(self, serialised : bool = False):
        """
        Deconstructs the whole object into a Python dictionary.

        Args:
            serialised (bool): Give a Python dictionary in serialised (True) form or deserialised (default = False).

        Notes:
            Functions and lambdas are always given in serialised form.

        Returns:
            dict: of object.
        """
        d = dict()
        for key, value in self.__dict__.items():
            if str(key).__contains__(self.__class__.__name__):
                continue
            if serialised and key in self.__meta_info.keys():
                d[key] = self.__meta_info[key]
            elif key in self.__meta_info.keys() and self.__meta_info[key]['type'] in ['function', 'lambda']:
                d[key] = self.__meta_info[key]
            elif isinstance(value, BasicRick):
                d[key] = value.dict(serialised=serialised)
            elif isinstance(value, list):
                new_list = list()
                for element in value:
                    if isinstance(element, BasicRick):
                        new_list.append(element.dict(serialised=serialised))
                    else:
                        new_list.append(element)
                d[key] = new_list
            else:
                d[key] = value
        return d

    def add_function(self, name, load, args : dict = None, imports : list = None ):
        """
        Add a new function to Rick.

        Args:
            name (str): Property name.
            load (str): Python code containing the function.
            args (dict): Key-value pairs of arguments with default values (default = None).
            imports (list): Python modules to import (default = None).

        Examples:
            Basic example for adding to a PickleRick:
                >> test_rick = PickleRick()

                >> load = '''
                        def tester(x, c):
                            y = x * 2 + c
                            return math.cos(y)
                        '''

                >> args = { 'x' : 0.42, 'c' : 1.7 }

                >> imports = ['math']

                >> test_rick.add_function('tester',load, args, imports)

                >> y = test_rick.tester(x=0.66, c=1.6)

        """
        if imports and isinstance(imports, list):
            for i in imports:
                if 'import' in i:
                    exec(i, globals())
                else:
                    exec('import {}'.format(i), globals())
        exec(load, globals())
        if args and isinstance(args, dict):
            arg_list = list()
            arg_list_defaults = list()
            for arg in args.keys():
                default_value = args[arg]
                if isinstance(default_value, str):
                    arg_list_defaults.append("{a}='{d}'".format(a=arg, d=default_value))
                else:
                    arg_list_defaults.append("{a}={d}".format(a=arg, d=default_value))
                arg_list.append('{a}={a}'.format(a=arg))

            func_string = 'lambda {args_default}: {name}({args})'.format(
                args_default=','.join(arg_list_defaults),
                args=','.join(arg_list),
                name=name)
        else:
            func_string = 'lambda: {name}()'.format(name=name)
        self.__dict__.update({name: eval(func_string)})
        self.__meta_info[name] = {'type' : 'function', 'name' : name, 'args' : args, 'import' : imports, 'load' : load}

    def add_lambda(self, name, load, imports : list = None ):
        """
        Add a Python lambda to Rick.

        Args:
            name (str): Property name.
            load (str): Python code containing the lambda.
            imports (list): Python modules to import (default = None).

        Examples:
            Basic example for adding to a PickleRick:
                >> test_rick = PickleRick()

                >> load = "lambda: dd.utcnow().strftime('%Y-%m-%d')"

                >> imports = ['from datetime import datetime as dd']

                >> test_rick.add_lambda('date_str', load, imports)

                >> date_string = test_rick.date_str()
        """
        if imports and isinstance(imports, list):
            for i in imports:
                if 'import' in i:
                    exec(i, globals())
                else:
                    exec('import {}'.format(i), globals())
        self.__dict__.update({name: eval(load)})
        self.__meta_info[name] = {'type' : 'lambda', 'import' : imports, 'load' : load}

    def add_env_variable(self, name, load, default = None):
        """
        Add a new OS ENVIRONMENT VARIABLE to Rick.

        Args:
            name (str): Property name.
            load (str): ENV var name.
            default (any): Default to value (default = None).
        """
        self.__dict__.update({name: os.getenv(load, default)})
        self.__meta_info[name] = {'type' : 'env', 'load' : load, 'default' : default}

    def add_base64(self, name, load):
        """
        Add Base 64 encoded binary data.

        Args:
            name (str): Property name.
            load (str): Base 64 encoded data.
        """
        b = base64.b64decode(load)
        self.__dict__.update({name: b})
        self.__meta_info[name] = {'type': 'base64',
                                  'load' : load
                                  }

    def add_csv_file(self,
                     name,
                     file_path : str,
                     fieldnames : list = None,
                     load_as_rick  : bool = False,
                     encoding : str = 'utf-8'
                     ):
        """
        Adds the ability to load CSV data as lists or even a list of Ricks where the column names are the properties.

        Args:
            name (str): Property name.
            file_path (str): File path to load from.
            fieldnames (list): Column headers (default = None).
            load_as_rick (bool): If true, loads and creates Rick from source, else loads the contents as text (default = False).
            encoding (str): If text, encoding can be specified (default = 'utf-8').

        """
        import csv
        with open(file_path, 'r', encoding=encoding) as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)
            l = list()

            if load_as_rick:
                csv_file = csv.DictReader(file, fieldnames=fieldnames, dialect=dialect)

                for row in csv_file:
                    l.append(dict(row))

                self._iternalize({name: l}, deep=True)
            else:
                csv_file = csv.reader(file, dialect=dialect)

                for row in csv_file:
                    l.append(row)

                self.__dict__.update({name: l})

        self.__meta_info[name] = {'type': 'from_csv',
                                  'file_path': file_path,
                                  'load_as_rick': load_as_rick,
                                  'fieldnames' : fieldnames,
                                  'encoding': encoding
                                  }

    def add_from_file(self, name,
                      file_path : str,
                      load_as_rick : bool = False,
                      deep : bool = False,
                      load_lambda : bool = False,
                      is_binary : bool = False,
                      encoding : str = 'utf-8'):
        """
        Adds the ability to further load Ricks from other YAML or JSON files, or alternatively load a text file.
        This opens up dynamic possibility, but with that it also opens up extreme security vulnerabilities.
        Only ever load files from trusted sources.
        **Important note: Even with ``deep`` and ``load_lambda`` set to False, further file or API calls could be found within the source that loads lambda functions.**
        **Important note: Be careful to never self-reference a file, i.e. don't load the same file from within itself to avoid infinte looping.**

        Args:
            name (str): Property name.
            file_path (str): File path to load from.
            load_as_rick (bool): If true, loads and creates Rick from source, else loads the contents as text (default = False).
            deep (bool): Internalize dictionary structures in lists (default = False).
            load_lambda (bool): Load lambda as code or strings (default = False).
            is_binary (bool): If the file is a binary file (default = False).
            encoding (str): If text, encoding can be specified (default = 'utf-8').
        """

        if load_as_rick and not is_binary:
            args = copy.copy(self.__init_args)
            args['load_lambda'] = load_lambda
            args['deep'] = deep
            self.__dict__.update({name: PickleRick(file_path, **args)})
        else:
            if is_binary:
                with open(file_path, 'rb') as fn:
                    self.__dict__.update({name: fn.read()})
            else:
                with open(file_path, 'r', encoding=encoding) as fn:
                    self.__dict__.update({name: fn.read()})

        self.__meta_info[name] = {'type': 'from_file',
                                  'file_path' : file_path,
                                  'load_as_rick' : load_as_rick,
                                  'deep' : deep,
                                  'load_lambda' : load_lambda,
                                  'is_binary' : is_binary,
                                  'encoding' : encoding
                                  }

    def add_html_page(self,
                      name,
                      url : str,
                      headers : dict = None,
                      params : dict = None,
                      expected_http_status : int = 200):
        """
        Loads HTML page as property.

        Args:
            name (str): Property name.
            url (str): URL to load from.
            headers (dict): Key-value pair for headers (default = None).
            params (dict): Key-value pair for parameters (default = None).
            expected_http_status (int): Should a none 200 code be expected (default = 200).

        """
        r = requests.get(url=url, params=params, headers=headers)

        if r.status_code == expected_http_status:
            self.__dict__.update({name: r.text})
        else:
            raise ValueError(f'Unexpected HTTP status code in response {r.status_code}')

        self.__meta_info[name] = {'type': 'html_page',
                                  'url': url,
                                  'headers': headers,
                                  'params': params,
                                  'expected_http_status': expected_http_status
                                  }

    def add_api_json_call(self, name,
                          url : str,
                          http_verb : str = 'GET',
                          headers : dict = None,
                          params : dict = None,
                          body : dict = None,
                          deep : bool = False,
                          load_lambda : bool = False,
                          expected_http_status : int = 200):
        """
        Load a JSON response from a URL and create a Rick from it. This opens up dynamic possibility,
        but with that it also opens up extreme security vulnerabilities. Only ever load JSON objects from trusted sources.
        **Important note: Even with ``deep`` and ``load_lambda`` set to False, further API calls could be found within the source that loads lambda functions.**
        **Important note: Be careful to never self-reference an API call, i.e. don't load the same API from within itself to avoid infinte looping.**

        Args:
            name (str): Property name.
            url (str): URL to load from.
            http_verb (str): Either 'POST' or 'GET' allowed (default = 'GET').
            headers (dict): Key-value pair for headers (default = None).
            params (dict): Key-value pair for parameters (default = None).
            body (dict): Key-value pair for data (default = None).
            deep (bool): Internalize dictionary structures in lists (default = False).
            load_lambda (bool): Load lambda as code or strings (default = False).
            expected_http_status (int): Should a none 200 code be expected (default = 200).

        """
        if http_verb.lower() == 'post':
            r = requests.post(url=url, data=body, headers=headers)
        else:
            r = requests.get(url=url, params=params, headers=headers)

        if r.status_code == expected_http_status:
            json_dict = r.json()
            args = copy.copy(self.__init_args)
            args['load_lambda'] = load_lambda
            args['deep'] = deep
            self.__dict__.update({name: PickleRick(json_dict, **args)})
        else:
            raise ValueError(f'Unexpected HTTP status code in response {r.status_code}')
        self.__meta_info[name] = {'type': 'api_json',
                                  'url': url,
                                  'http_verb': http_verb,
                                  'headers' : headers,
                                  'params' : params,
                                  'body' : body,
                                  'deep' : deep,
                                  'load_lambda' : load_lambda,
                                  'expected_http_status' : expected_http_status
                                  }
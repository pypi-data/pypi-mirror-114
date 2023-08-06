# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fromjson']
setup_kwargs = {
    'name': 'fromjson',
    'version': '0.1.0',
    'description': 'Easily read objects from json',
    'long_description': '# fromjson\n\nPython library to easily read objects from JSON.\n\nHave you ever had classes, which you want to read from JSON, but didn\'t want to write the boilerplate `from_json` classmethods to convert JSON to Python objects?\nNow you don\'t have to!\nfromjson adds a simple decorator for classes, which adds a `from_json` classmethod to the class.\nIt works on all classes, as long as the fields in the class are either Python primitive types (int, float, str, dict, list) or classes with a `from_json` classmethod, and the class has type hints for its constuctor.\nThis means that if you have nested classes which you want to load from JSON, you only need to add a decorator call for each of the classes.\n\nThis library is heavily inspired by the excellent Haskell library [aeson](https://hackage.haskell.org/package/aeson).\n\n## Usage\n\nAll the examples have these imports\n```\n>>> from dataclasses import dataclass\n>>> import json\n>>>\n>>> from fromjson import fromjson, tojson\n\n```\nSuppose we have the following JSON:\n\n```{python}\n>>> foo = """\n... {\n...   "field": "a string value",\n...   "another_field": 42\n... }\n... """\n\n```\n\nWe want to deserialise it into a class defined by:\n\n```{python}\n>>> @dataclass\n... class Foo:\n...     field: str\n...     another_field: int\n\n```\n\nAdding a `@fromjson` decorator before the class definition adds a `from_json` classmethod to the class, which enables us to load it from a dictionary representation:\n\n```\n>>> @dataclass\n... @fromjson\n... class Foo:\n...     field: str\n...     another_field: int\n...\n>>> Foo.from_json(json.loads(foo))\nFoo(field=\'a string value\', another_field=42)\n\n```\n\n## `tojson`\n\nFor completeness, there\'s also a `@tojson` decorator, which does the opposite.\nIt is used similarly:\n\n```{python}\n>>> @dataclass\n... @tojson\n... class Foo:\n...     field: str\n...     another_field: int\n...\n>>> json.dumps(Foo("asd", 42).to_json())\n\'{"field": "asd", "another_field": 42}\'\n\n```\n\n## Nested classes\n\nThe real power of fromjson is in deserialising user made classes, which have other user made classes as fields.\nSuppose we have the following nested JSON data:\n\n```\n>>> bird = """\n... {\n...     "name": "Duck",\n...     "cry": "Quack!",\n...     "egg": {\n...       "size": "Medium",\n...       "color": "White"\n...     }\n... }\n... """\n\n```\n\nWe can parse it into the following classes, by adding a `@fromjson` call to each class:\n```\n>>> @dataclass\n... @fromjson\n... class Egg:\n...     size: str\n...     color: str\n...\n>>> @dataclass\n... @fromjson\n... class Bird:\n...     name: str\n...     cry: str\n...     egg: Egg\n...\n>>> import json\n>>> Bird.from_json(json.loads(bird))\nBird(name=\'Duck\', cry=\'Quack!\', egg=Egg(size=\'Medium\', color=\'White\'))\n\n```\n\n## Parsing logic\n\nThe json is parsed according to the following logic:\n- The argument for `from_json` has to be a `Mapping` (i.e. an ordinary dictionary is fine)\n- The type hints for the class are read\n- For each type hint, if the type is one of `str`, `int`, `float`, `dict`, or `list`, the corresponding value from the argument mapping is used as-is.\n- If the type is none of the enumerated primitive types, it has to be a class with a `from_json` classmethod, which is then used to parse the object.\n- If the type isn\'t a primitive, and the class doesn\'t have a `from_json` classmethod, the parsing fails.\n\nIf your nested class has some really complicated parsing logic, for which `fromjson` is inadequate, you can write a `from_json` classmethod by hand.\nThen the class can be used inside other classes, which have a `@fromjson` decorator call.\n\n',
    'author': 'Lassi Haasio',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~ilikeavocadoes/fromjson',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

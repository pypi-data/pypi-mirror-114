# fromjson

Python library to easily read objects from JSON.

Have you ever had classes, which you want to read from JSON, but didn't want to write the boilerplate `from_json` classmethods to convert JSON to Python objects?
Now you don't have to!
fromjson adds a simple decorator for classes, which adds a `from_json` classmethod to the class.
It works on all classes, as long as the fields in the class are either Python primitive types (int, float, str, dict, list) or classes with a `from_json` classmethod, and the class has type hints for its constuctor.
This means that if you have nested classes which you want to load from JSON, you only need to add a decorator call for each of the classes.

This library is heavily inspired by the excellent Haskell library [aeson](https://hackage.haskell.org/package/aeson).

## Usage

All the examples have these imports
```
>>> from dataclasses import dataclass
>>> import json
>>>
>>> from fromjson import fromjson, tojson

```
Suppose we have the following JSON:

```{python}
>>> foo = """
... {
...   "field": "a string value",
...   "another_field": 42
... }
... """

```

We want to deserialise it into a class defined by:

```{python}
>>> @dataclass
... class Foo:
...     field: str
...     another_field: int

```

Adding a `@fromjson` decorator before the class definition adds a `from_json` classmethod to the class, which enables us to load it from a dictionary representation:

```
>>> @dataclass
... @fromjson
... class Foo:
...     field: str
...     another_field: int
...
>>> Foo.from_json(json.loads(foo))
Foo(field='a string value', another_field=42)

```

## `tojson`

For completeness, there's also a `@tojson` decorator, which does the opposite.
It is used similarly:

```{python}
>>> @dataclass
... @tojson
... class Foo:
...     field: str
...     another_field: int
...
>>> json.dumps(Foo("asd", 42).to_json())
'{"field": "asd", "another_field": 42}'

```

## Nested classes

The real power of fromjson is in deserialising user made classes, which have other user made classes as fields.
Suppose we have the following nested JSON data:

```
>>> bird = """
... {
...     "name": "Duck",
...     "cry": "Quack!",
...     "egg": {
...       "size": "Medium",
...       "color": "White"
...     }
... }
... """

```

We can parse it into the following classes, by adding a `@fromjson` call to each class:
```
>>> @dataclass
... @fromjson
... class Egg:
...     size: str
...     color: str
...
>>> @dataclass
... @fromjson
... class Bird:
...     name: str
...     cry: str
...     egg: Egg
...
>>> import json
>>> Bird.from_json(json.loads(bird))
Bird(name='Duck', cry='Quack!', egg=Egg(size='Medium', color='White'))

```

## Parsing logic

The json is parsed according to the following logic:
- The argument for `from_json` has to be a `Mapping` (i.e. an ordinary dictionary is fine)
- The type hints for the class are read
- For each type hint, if the type is one of `str`, `int`, `float`, `dict`, or `list`, the corresponding value from the argument mapping is used as-is.
- If the type is none of the enumerated primitive types, it has to be a class with a `from_json` classmethod, which is then used to parse the object.
- If the type isn't a primitive, and the class doesn't have a `from_json` classmethod, the parsing fails.

If your nested class has some really complicated parsing logic, for which `fromjson` is inadequate, you can write a `from_json` classmethod by hand.
Then the class can be used inside other classes, which have a `@fromjson` decorator call.


# Maceió
Package to insert JSON data into a SQL database.

## What it does
In short, given a JSON input, Maceio is able to:
- Create, and populate, a new table based on a JSON input (no need to specify its structure)
- Feed JSON records into an existing table (inserting a new register or updating existing ones)

## Getting Started

### 1. No structure, no db options (quick option)
```python
from Maceio.Maceio import Maceio

if __name__ == "__main__":
    # You can use only one dictionary without lists
    data = '''[
            {
                "field1":{
                    "subfield1": 1,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 1",
                        "sub2":"Value 2",
                    }
                }
            },
            {
                "field1":{
                    "subfield1": 2,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 3",
                        "sub2":"Value 4",
                    }
                }
            }
        ]
    ''')

    maceio = Maceio('postgresql+psycopg2://user:password@host:port/database', 'schema_example')
    maceio.save('table_example', data, conflicts=('subfield1', 'subfield2'))
```


### 2. Adding db options (connection limits and pool size)

```python
from Maceio.Maceio import Maceio

if __name__ == "__main__":
    # You can use only one dictionary without lists
    data = '''[
            {
                "field1":{
                    "subfield1": 1,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 1",
                        "sub2":"Value 2",
                    }
                }
            },
            {
                "field1":{
                    "subfield1": 2,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 3",
                        "sub2":"Value 4",
                    }
                }
            }
        ]
    ''')
    maceio = Maceio('postgresql+psycopg2://user:password@host:port/database', 'schema_example', pool_size=5, max_overflow=2)
    maceio.save('table_example', data, conflicts=('subfield1', 'subfield2'))
```

### 3. Disabling table existence check

```python
from Maceio.Maceio import Maceio

if __name__ == "__main__":
    # You can use only one dictionary without lists
    data = '''[
            {
                "field1":{
                    "subfield1": 1,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 1",
                        "sub2":"Value 2",
                    }
                }
            },
            {
                "field1":{
                    "subfield1": 2,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 3",
                        "sub2":"Value 4",
                    }
                }
            }
        ]
    ''')
    maceio = Maceio('postgresql+psycopg2://user:password@host:port/database', 'schema_example', pool_size=5, max_overflow=2)

    # To not check if table exists, set verify=False
    maceio.save('table_example', data, conflicts=('subfield1', 'subfield2'), verify=False, primaries=('id',))
```

### Disabling JSON format

```python
from Maceio.Maceio import Maceio

if __name__ == "__main__":
    # You can use only one dictionary without lists
    data = '''[
            {
                "field1":{
                    "subfield1": 1,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 1",
                        "sub2":"Value 2",
                    }
                }
            },
            {
                "field1":{
                    "subfield1": 2,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 3",
                        "sub2":"Value 4",
                    }
                }
            }
        ]
    ''')

    # Passing enableJsonType=False disables storing with JSON type, so JSON data will be saved as string instead
    maceio = Maceio('postgresql+psycopg2://user:password@host:port/database', 'schema_example', pool_size=5, max_overflow=2, enableJsonType=False)
    maceio.save('table_example', data, conflicts=('subfield1', 'subfield2'), verify=True, primaries=('id',))
```

### Saving all data types as string instead
This can be particularly useful for initial exploration of data with unknown data types.

```python
from Maceio.Maceio import Maceio

if __name__ == "__main__":
    # You can use only one dictionary without lists
    data = '''[
            {
                "field1":{
                    "subfield1": 1,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 1",
                        "sub2":"Value 2",
                    }
                }
            },
            {
                "field1":{
                    "subfield1": 2,
                    "subfield2": "TYPE1",
                    "subfield3":{
                        "sub1":"Value 3",
                        "sub2":"Value 4",
                    }
                }
            }
        ]
    ''')

    # To save all formats as string, pass onlyText=True
    maceio = Maceio('postgresql+psycopg2://user:password@host:port/database', 'schema_example', pool_size=5, max_overflow=2, onlyText=True)
    maceio.save('table_example', data, conflicts=('subfield1', 'subfield2'), verify=True, primaries=('id',))
```
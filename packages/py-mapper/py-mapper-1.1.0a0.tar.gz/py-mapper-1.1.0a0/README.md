# py-mapper
Python Mapper Library

### How to use this library

##### 1. Mapping Flat Dictionary

```Python
from pymapper import Mapper

mapper = Mapper({
    'dest_1': '$source_1',
    'dest_2': '$source_2'
})

result = mapper.map({
    'source_1': 1,
    'source_2': 'Lorem ipsum',
    'source_3': 3.4
})
# result = {'dest_1': 1, 'dest_2': 'Lorem ipsum'}
```

##### 2. Mapping Nested Dictionary

```Python
from pymapper import Mapper

mapper = Mapper({
    'dest_1': {
        'dest_2': '$source_1.source_2'
    },
    'dest_2': '$source_1.source_3.source_4'
})

result = mapper.map({
    'source_1': {
        'source_2': [1, 2, 3],
        'source_3': {
            'source_4': 5
        }
    },
})
# result = {'dest_1': {'dest_2': [1, 2, 3]}, 'dest_2': 5}
```

##### 3. Mapping a List of Dictionaries

```Python
from pymapper import Mapper

mapper = Mapper({
    'dest_1': {
        'dest_2': '$source_1.source_2'
    },
    'dest_2': '$source_1.source_3.source_4'
})

result = mapper.map([
    {
        'source_1': {
            'source_2': [1, 2, 3],
            'source_3': {
                'source_4': 5
            }
        }
    },
    {
        'source_1': {
            'source_2': [4, 5, 6],
            'source_3': {
                'source_4': 7
            }
        }
    }
])
# result = [{'dest_1': {'dest_2': [1, 2, 3]}, 'dest_2': 5}, {'dest_1': {'dest_2': [4, 5, 6]}, 'dest_2': 7}]
```
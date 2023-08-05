# configini
Small package to easily parse an .ini file.

## Read values
#### config.ini
```ini
[chapter]
key=hello world
```
Import the configini module into your _config.py_ file.
Then read the _config.ini_ file, 
and fetch the values from the configini module.
#### config.py:
```python
import configini

# Read the config.ini file.
configini.read('config.ini')

class Config:
    # Set value1 to [chapter] => key
    value = configini.get('chapter', 'key')

```
Then you can use your config variables like this:
#### example.py:
```python
# Import the config file
from config import Config

# Do whatever you want with it.
some_variable = Config.value1
```

## Cast data types
To cast values to different data types. you can set the parameter _date_type_
#### config.ini:
```ini
[chapter]
number=2
decimal=6.2
boolean=true
list=["A", "B", "C"]
```

#### config.py:
```python
import configini

class Config:
    str_value = configini.String('test', 'test_str')
    int_value = configini.Integer('test', 'test_int')
    float_value = configini.Float('test', 'test_float')
    dec_value = configini.Decimal('test', 'test_dec')
    bool_value = configini.Boolean('test', 'test_bool')
    list_value = configini.List('test', 'test_list')
    dict_value = configini.Dict('test', 'test_dict')
    var_value = configini.Variable('test', 'test_var', str, 'Test')
    datetime_value = configini.DateTime('test', 'test_datetime')
    date_value = configini.DateTime('test', 'test_date', format='%Y-%m-%d')
    time_value = configini.DateTime('test', 'test_time', format='%H:%M')
```

**Note:** If _data_type_ is set to _bool_, only empty values, '0' and 'false' will be cast to False.\
**Note:** Only use double quote for strings inside list, the json.loads() method is used for parsing to list.

## default values
Default values will be used when the value inside the configurations file is empty.
You can change the default value by passing the _default_ parameter.
```python
import configini

class Config:
    value = configini.String('chapter', 'key', default='Hello world')
```

## custom values
Default values will be used when the value inside the configurations file is empty.
You can change the default value by passing the _default_ parameter.
```python
import configini
import uuid

class Config:
    value = configini.String('chapter', 'key', default='Hello world')
```
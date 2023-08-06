ServiceNowPy
============

A library that helps you to get data from ServiceNow's Table API.

Installation
------------

```console
$ pip install servicenowpy
```

Simple usage
------------

How to retrieve data from incident table with this lib:

```python
>>> from servicenowpy import ServiceNow
>>> snow = ServiceNow('dev01010', 'admin', 'password')
>>> inc_table = snow.get_table('incident', sysparm_fields='number,short_description')
>>> for record in inc_table.records:
...     print(record)
{'number': 'INC0000060', 'short_description': 'Unable to connect to email'}
{'number': 'INC0000009', 'short_description': 'Reset my password'}
{'number': 'INC0009005', 'short_description': 'Need access to the common drive'}
```
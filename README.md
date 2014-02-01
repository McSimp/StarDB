# StarDB

A Python library for manipulating Starbound database files. The code is loosely 
based on [yuedb](https://bitbucket.org/kyren/yuedb), which is written by one of 
the Starbound developers and is what the DB code in the game is based on as 
well.

Currently StarDB only supports read operations, but write operations may be 
added in the future.

## Usage

From a user's perspective, a database works in the same way that a Python 
dictionary does: a key-value store. The internal implementation is largely 
irrelevant.

Here's an example for listing the files in an AssetDatabase, then reading the 
contents of the `/weather/snow/snow.weather` key:

```python
from stardb.storage import BlockFile
from stardb.databases import AssetDatabase

bf = BlockFile(open('packed.pak', 'rb'))
db = AssetDatabase(bf)
db.open()

print(db.getFileList())
print(db['/weather/snow/snow.weather'])
```

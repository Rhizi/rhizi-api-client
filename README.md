# Rhizi Importer

Client to import data into Rhizi nodes

## Using Python
```python
from client import RhiziAPIClient
client = RhiziAPIClient("http://localhost:8080")
client.login_user("test@test.com", "password")
client.create_node("ID-89388", data={"type"="Typed", "title"="The Most Awesome Title"})
client.create_node("ID-89389", data={"type"="Typed", "title"="The Second Most Awesome Title"})
client.create_edge("ID-89389", "ID-89388")
```

## Using Command-line

```bash
$ python import_to_rhizi.py
Rhizi Importer with simples options
usage: import_to_rhizi.py [-h] [--base-url BASE_URL]
[--user USER] [--password PASSWORD] filename

positional arguments:
  filename             CSV file path

optional arguments:
  -h, --help           show this help message and exit
  --base-url BASE_URL  Base URL for the API
  --user USER          Username
  --password PASSWORD  password
```

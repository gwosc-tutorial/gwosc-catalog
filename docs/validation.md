
# Validate schema

## Using the command line

The installation step will install a CLI program named `validateschema` that can be used to validate your JSON file.

```shell
validateschema path/to/mycatalog.json
```

If `stdout` outputs no errors, the schema passed validation.

## Using the library

You can also validate a file or a python dictionary using the library

```python
import json
from gwosc_catalog import validate_schema

with open("path/to/mycatalog.json") as fp:
    cat = json.load(fp)
validate_schema(cat)
```

Or if you have a python dictionary object `my_catalog_dict`:

```python
from gwosc_catalog import Catalog
cat = Catalog.from_json(my_catalog_dict)
```

The catalog is valid if no errors were raised.

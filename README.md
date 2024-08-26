# GWOSC Catalog Schema

[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://gwosc-tutorial.github.io/gwosc-catalog/)

The GWOSC Catalog Schema is a simple versioned JSON schema that is intended to be consumed for publication by the GWOSC backend.

This package provides utilities for creating and validating community catalogs JSON schema.

## Installation

1. Clone repo

    ```
    git clone git@github.com:gwosc-tutorial/gwosc-catalog.git
    ```

2. Install

    ```
    cd gwosc-catalog; pip install .
    ```

## Validate upload schema

To validate the schema, the library also installs the `validateschema` CLI program.

```
validateschema path/to/mycatalog.json
```

If `stdout` outputs no errors, the schema passed validation.

## Documentation

For more information on the schema and how to use validation tools, [please refer to the documentation](https://gwosc-tutorial.github.io/gwosc-catalog/).

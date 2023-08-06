# Swaggertest

This is a very simple tool which tests swagger (OpenAPI) 
specifications. In particular, it checks the schemas provided
in the 'components/schemas' section of the document against
any examples provided along with the schemas.

## Installation

```bash
$ pip install swaggertest
```

## Usage

```bash
$ swaggertest --help
usage: swaggertest [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]
[--pdb]

Swagger testing tool

optional arguments:
  --version            show program's version number and exit
  -v, --verbose        Increase verbosity of output. Can be repeated.
  -q, --quiet          Suppress output except warnings and errors.
  --log-file LOG_FILE  Specify a file to log output. Disabled by default.
  -h, --help           Show help message and exit.
  --debug              Show tracebacks on errors.
  --pdb

Commands:
  complete       print bash completion command (cliff)
  help           print detailed help for another command (cliff)
  test-schemas   Validate examples against schemas
```

The main sub-command is `test-schemas`:

```bash
$ swaggertest help test-schemas
usage: swaggertest test-schemas [-h] [-d] [-p PATH] [-s] filename

Validate examples against schemas

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  -d, --detail
  -p PATH, --path PATH  Path to where the schemas are located
  -s, --strict          Default to 'allowExtraProperties: false'
```

To test a spec, just provide it as the `filename` argument. You can also
provide a path argument to specify where the schemas are to be found:

```bash
$ swaggertest test petstore.json --path '/definitions' --detail --strict
Validated 6 schemas:
  - 0 had errors
```

<div align="center">
  <img src="https://imgur.com/FgQvEZ2.png" /><br><br>
</div>

# savvihub-client [![pypi](https://img.shields.io/pypi/v/savvihub.svg)](https://pypi.python.org/pypi/savvihub)

A Command line interface and library for SavviHub


## Features
- A Command line interface to communicate with SavviHub
- Python SDK to log the experiment

## How to develop
### Prerequisites
* Python (3.8.x is recommended.)
* [openapi-generator](https://github.com/OpenAPITools/openapi-generator)
    ```shell
    $ brew install openapi-generator
    ```

### Environment variable setting
* Add backend URL
  ```shell
  # Port can be different from user's setting
  export SAVVIHUB_WEB_HOST=http://localhost:3000
  ```
* Add frontend URL
  ```shell
  # Port can be different from user's setting
  export SAVVIHUB_API_HOST=http://localhost:10000
  ```

### Entrypoint
```angular2html
cd savvihub-client/savvihub/cli/commands
python main.py {command} {options}
```

## Quickstart
```shell
pip install savvihub
```

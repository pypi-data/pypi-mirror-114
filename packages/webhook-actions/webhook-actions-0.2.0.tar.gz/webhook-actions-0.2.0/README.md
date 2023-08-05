# Webhook Actions

[![python](https://img.shields.io/pypi/pyversions/webhook-actions.svg)](https://pypi.python.org/pypi/webhook-actions)
[![Latest PyPI version](https://img.shields.io/pypi/v/webhook-actions.svg)](https://pypi.python.org/pypi/webhook-actions)
[![Downloads](https://pepy.tech/badge/webhook-actions)](https://pepy.tech/project/webhook-actions?right_color=orange)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Senth/webhook-actions.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Senth/webhook-actions/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Senth/webhook-actions.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Senth/webhook-actions/context:python)

Webhook that runs scripts located in `~/webhook-actions/` directory.

## How To Use

1. Add scripts into webhook-actions. These can be in sub-directories
1. Call the URL `http://localhost:5000/your-script-name`

### Simple example

- **URL:** `http://localhost:5000/log-stat`
- **Body:** something
- **Command:** `~/webhook-actions/log-stat something`

### Example with subdirectories

- **URL:** `https://YOUR_DOMAIM.com/git/your-project/deploy`
- **Body:** {"tag": "1.0.1"}
- **Command:** `~/webhook-actions/git/your-project/deploy "{\"tag\": \"1.0.1\"}"`

## Example config file

The config file is located at `~/.webhook-actions.cgf`.
When you run the script the first time it will create a default configuration.

```ini
[General]
# Port to listen to
Port = 5000
```

## Authors

- Matteus Magnusson, senth.wallace@gmail.com

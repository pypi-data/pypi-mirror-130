# drf_spectacular_extensions
[![PyPI Version][pypi-image]][pypi-url]

[pypi-image]: https://img.shields.io/pypi/v/drf_spectacular_extensions
[pypi-url]: https://pypi.org/project/drf_spectacular_extensions/

# Installation

Using pip

`pip install drf_spectacular_extensions`

Using pipenv

`pipenv install drf_spectacular_extensions`

# Quick start
In your project’s `settings.py`.

```
SPECTACULAR_SETTINGS: Dict[str, Any] = {
    ...
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular_extensions.postprocessing_hooks.add_servers",
    ]
}
```

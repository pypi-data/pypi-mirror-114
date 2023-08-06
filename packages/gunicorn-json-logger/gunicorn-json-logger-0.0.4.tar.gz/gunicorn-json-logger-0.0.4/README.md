# gunicorn-json-logger

Gunicorn log configuration for all Attuned Python services

Part of ATTUNED-2597 and DataDog integration.

# Getting Started

```
pip install gunicorn-json-logger
```

In your gunicorn configuration file (`.py`), add the following lines:

```
from gunicorn-json-logger.config import get_log_config

# Gunicorn config variables
logconfig_dict = get_log_config
# ... other configs ...
```
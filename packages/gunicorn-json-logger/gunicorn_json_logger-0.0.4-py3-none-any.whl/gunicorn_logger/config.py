__all__ = (
    "get_log_config",
    "JSON_FIELDS"
)

JSON_FIELDS = (
    "asctime", "message", "name", "created",
    "filename", "module", "funcName", "lineno",
    "msecs", "pathname", "process", "processName",
    "relativeCreated", "thread", "threadName", "levelname",
    "access",
)


def build_log_format(fields):
    return " ".join(f"%({f})s" for f in fields)


def get_log_config(fields=JSON_FIELDS):
    """
    Get log config for Gunicorn+Uvicorn
    """
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                "format": build_log_format(fields=fields),
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'json',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
            'stderr': {
                'level': 'NOTSET',
                'formatter': 'json',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'WARNING',
            },
            'gunicorn.error': {
                'handlers': ['stderr'],
                'level': 'INFO',
                'propagate': False,
            },
            'gunicorn': {
                'handlers': [],
                'level': 'NOTSET',
                'propagate': True,
            },
            'gunicorn.access': {
                'handlers': [],
                'level': 'INFO',
                'propagate': False,
            },
            'gunicorn.http.asgi': {
                'handlers': [],
                'level': 'NOTSET',
                'propagate': True,
            },
            'gunicorn.http': {
                'handlers': [],
                'level': 'NOTSET',
                'propagate': True,
            },
            "uvicorn": {
                'handlers': [],
                'level': 'NOTSET',
                'propagate': True,
            },
            "uvicorn.error": {
                'handlers': ['stderr'],
                'level': 'INFO',
                'propagate': True,
            },
            "uvicorn.access": {
                "handlers": [],
                "level": 'INFO',
                "propagate": True
            },
        }
    }

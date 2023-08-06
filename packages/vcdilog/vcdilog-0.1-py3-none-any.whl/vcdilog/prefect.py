import os


def get_prefect_logger(name):
    import prefect

    return prefect.context.get(name)


def set_prefect_extra_loggers(loggers_list):
    formatted = repr(loggers_list)

    VAR = "PREFECT__LOGGING__EXTRA_LOGGERS"
    os.environ[VAR] = formatted

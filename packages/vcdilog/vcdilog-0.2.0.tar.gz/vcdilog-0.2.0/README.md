# vcdilog: logging as easy as print statements

You almost certainly should be using log statement instead of messy print statements. `vcdilog` makes this easy.


## Install

You can install `vcdilog` using pip:

```
$ pip install vcdilog
```

If using poetry, simply add this line to your `pyproject.toml` file.

```
vcdilog = "*"
```

## Philosophy

The built in python logging library is highly customizable, but hard to visualize and understand. `vcdilog` doesn't try to replace what is in the standard library, but streamlines it with sensible defaults.


## Basic, instead-of-print-statements usage

All you need is two lines of setup: One import, and one line to add a handler for stdout/stderr output.

```
from vcdilog import log
log.add_std_handler()

log.info('hello world')  # .info, .warning, .debug, etc
```


## More flexible usage

You can create a log object:

```
from vcdilog import Logger

log = Logger()
```

Crucially, you don’t need to give the logger a name, it will figure out the current module name automatically and use that. This same method is used by the print-statements example above - they'll be logged to an appropriately-named logger automatically, based on the module they're in.

You can set a log level with:

```
log.set_level(level="DEBUG")
```

DEBUG means all logged messages will actually get logged. When you add a handler with e.g. `add_std_handler`, the handler will be assigned the `DEBUG` level by default, and so will the associated logger.

For production usage, a lower level should ordinarily be set to avoid overly verbose logging.


## Other handlers

So far three handlers are supported.

```
x.add_std_handler()
x.add_null_handler()
x.add_json_handler()
```

As per the above, the standard output handler logs to the console. It uses some customization log errors to stderr and normal messages to stdout, just like `print()` does, which means you can use logging calls instead of print statements.

The null handler should be used in libraries - it’s best practice when publishing a library to create a logger but add only a null handler and no others to that users of the library don’t get unwanted log messages (if they want to see them, they’ll add their own handlers).

Then there’s the json handler. That logs json-formatted log items to a file.

For instance, the following:

```
log.info("classic message", extra={"special": "value", "run": 12})
```

Will result in:

```
{"message": "classic message", "special": "value", "run": 12}
```

In the log file (log.json by default)

## Basic prefect support

Getting a prefect logger is as easy as:

```
prefect_logger = vcdilog.get_prefect_logger()
```

and you can do...

```
vcdilog.set_prefect_extra_loggers(['boto3', 'whatever'])
```

to have those loggers inherit the prefect logging config.

More prefect support is on the way!
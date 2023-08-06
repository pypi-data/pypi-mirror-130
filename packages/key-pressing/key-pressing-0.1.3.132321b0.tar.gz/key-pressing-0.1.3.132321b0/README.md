# print_function_py2

## Usage

This package is using for detect pressing in Python.

## How to use it

Import it by: `import key_pressing`. No any additional modules or packages will be installed. You need to install bash if you are using POSIX.

```python2
>>> import key_pressing
>>> key_pressing.detect_onekey()
O
'O'
>>> key_pressing.detect_escape()
^[[7m
'\x1b[7m'
>>> key_pressing.detect_keys(12)
Hello world!
'Hello world!'
```

If you cannot install the package by pip, please download the tar.gz file and extract to sys.path(PYTHONPATH).

## Known issues

* Cannot be used on Win32 platform.
* Cannot detect newline character correctly(got it as `\x00`).

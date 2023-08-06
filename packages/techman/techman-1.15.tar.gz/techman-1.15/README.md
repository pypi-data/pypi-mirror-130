# `techman.py`

General Purpose Python Library by @Techman55

----

## How to Import

```
try:
    import techman
except ModuleNotFoundError:
    import sys, subprocess
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'techman'])
```

----

## `techman.py` Flag for Your Project's `README.md`

```
> This program uses the `techman.py` general purpose python library. [Learn more](https://py.techmandev.com)
```

#### Example

> This program uses the `techman.py` general purpose python library. [Learn more](https://py.techmandev.com)


-----
<br><br>

## Classes


### yn

User input gatherer for Yes/No questions using `input()`

#### `yn.ask()`
#### `yn.check()`

---

### QuickSetup

Simple App data and "is first open" tracker

#### `is_first_open()`

#### `reset_first_open()`

#### `does_config_exist()`

#### `write_config()`

#### `read_config()`

#### `update_config()`

#### `reset_config()`


---

### Packages

Easy functions to manage packages from pip

#### `is_package_installed()`

#### `install()`

---
### Functions

Assorted functions that don't fit into a class

#### `set_clipboard()`

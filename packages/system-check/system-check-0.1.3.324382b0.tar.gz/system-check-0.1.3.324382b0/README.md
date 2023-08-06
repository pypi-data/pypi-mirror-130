# system-check

## Usage

This package is using for check Python properties.

## How to use it

Import it by: `from syschk import *`. No any additional modules or packages will be installed.

To check is there a variable named `True` :
```python3
from syschk import *
check_exists("True") # Returns 1 if it exists
```

To check what is the value of `sys.version` :
```python3
from syschk import *
import sys
check_value("sys.version")
```

To check is there a module named `threading` :
```python3
from syschk import *
check_run("import threading") # This will not be really imported because it's in a function
```

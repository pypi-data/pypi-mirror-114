# scanfs

This module scans the filesystem and provides custom hooks to handle each file
type of your choice.

## Installation

```bash
pip install scanfs
```

## Example

### How to write your own scanner enhancements?

This example scans the `/usr/bin` folder for ELF files and handles the callback
to provide file stat info.

```python
import os
from scanfs.fsscanner import FileSystemScanner
from scanfs.fsscannerex import FSScannerException


def callback(fpath, node):
    try:
        path = os.path.join(fpath, node.name)
        # Now do what you want on the instance of file
        # eg. stat
        statinfo = os.stat(path)
        print(statinfo)
    except FSScannerException as e:
        print("An exception occurred: " + str(e))


fss = FileSystemScanner("/usr/bin")
fss.scan_for_elfs(callback)
```

### Simple way to scan ELF files for binary protection check using `checksec` utility

> `checksec` utility can be downloaded [here](https://github.com/slimm609/checksec.sh)

```python
import os
import subprocess
from scanfs.fsscanner import FileSystemScanner
from scanfs.scanners.checksecscanner import CheckSecScanner

css = CheckSecScanner("/usr/bin", "/tmp/checksec_results.json")
css.checksec_on_elfs()

css = CheckSecScanner("/usr/bin", "/tmp/checksec_results.csv", fformat="csv")
css.checksec_on_elfs()
```

## Developer

```bash
python -m build
twine upload dist/*
```

> Ref: https://packaging.python.org/tutorials/packaging-projects/

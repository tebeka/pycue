# pycue - Python Wrapper for https://cuelang.org

![cue](https://github.com/tebeka/cue/workflows/cue/badge.svg)

**Alpha release - use at your own risk**


## Examples

```python

import cue
import yaml

# Use over files
cue.vet.files('schema.cue', 'data.yml')  # Will raise cue.Error on errors

# Use Validator
with open('data.yml') as fp:
    obj = yaml.safe_load(fp)

v = cue.Validator.from_file('schema.cue')
v.validate(obj)
```

## Install

`python -m pip install pycue`

This library uses the `cue` command line utility and will fail if it's not found in PATH.
You can set the `CUE_EXE` environment variable if you have non-standard `cue` install.

Run `cue.check_install()` to validate installation.

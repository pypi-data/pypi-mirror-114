# Python Thycotic
This is a Python wrapper for Thycotic Secret Server API version 10.9.

## Install
```shell
pip install python_thycotic
```

## Usage
You will need to the username, password, and Thycotic Secret Server URL to instantiate the class.
```python
import os, thycotic
ss = thycotic.Api(
    os.environ.get("THYCOTIC_USER"),
    os.environ.get("THYCOTIC_PASS"),
    os.environ.get("THYCOTIC_URL"),
)
```

Get an access token, which is used to make API calls
```python
ss.auth()
```

Get a secret by id
```python
secret = ss.get_secret(123)
```

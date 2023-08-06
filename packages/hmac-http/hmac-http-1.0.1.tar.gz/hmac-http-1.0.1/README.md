# hmac-http
[![build status](https://img.shields.io/drone/build/hwittenborn/hmac-http/main?logo=drone&server=https%3A%2F%2Fdrone.hunterwittenborn.com)](https://drone.hunterwittenborn.com/hwittenborn/hmac-http/latest)
[![PyPI](https://img.shields.io/pypi/v/hmac-http?logo=pypi)](https://pypi.org/project/hmac-http/)

Python 3 library for the `draft-cavage-http-signatures-10` specification.

## Usage
Currently, only verifying requests is supported.

To verify requests, run `hmac_http.verify(request, secret)` function, where `request` is a request from an ASGI-based application, and `secret` is the secret shared between the client and reciever:

```python3
from hmac_http import verify
secret = "asdf"

verify(request, secret)
```

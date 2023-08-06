# TimeChimp
![Build](https://github.com/Afilnor/TimeChimp/actions/workflows/python-publish.yml/badge.svg)
[![codecov](https://codecov.io/gh/Afilnor/TimeChimp/branch/master/graph/badge.svg?token=O2VKP0JNH7)](https://codecov.io/gh/Afilnor/TimeChimp)
![License](https://img.shields.io/github/license/Afilnor/TimeChimp)
## Description
- SDK to interact with TimeChimp API
- Can return a converted response to JSON and check for errors.
- Log HTTP method, url, params and headers
- Hide access_token in the logs

## How to install
`pip3 install timechimp`

## Documentation

https://timechimp.readthedocs.io/en/latest/

## Source structure
- _endpoint.py: contain the source endpoints.
- _env_variables.py: env variables names holding the auth value (eg API token).
- api sub-package contains the functions to call

## How to use

- access token is retrieved through env variables TIMECHIMP_ACCESS_TOKEN

### Get the requests response object
```
import timechimp

response = timechimp.api.users.get_all()
```

### Convert the response object to json
```
import timechimp

users = timechimp.api.users.get_all(to_json=True)
```

## Test
`pytest`

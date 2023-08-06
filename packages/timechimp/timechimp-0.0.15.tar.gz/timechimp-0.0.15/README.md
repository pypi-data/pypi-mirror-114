# TimeChimp
![Build](https://github.com/Afilnor/TimeChimp/actions/workflows/build_master.yml/badge.svg)
![Doc](https://readthedocs.org/projects/timechimp/badge/)
[![codecov](https://codecov.io/gh/Afilnor/TimeChimp/branch/master/graph/badge.svg?token=O2VKP0JNH7)](https://codecov.io/gh/Afilnor/TimeChimp)
![License](https://img.shields.io/github/license/Afilnor/TimeChimp)
[![PyPI version](https://badge.fury.io/py/timechimp.svg)](https://badge.fury.io/py/timechimp)
[![Downloads](https://pepy.tech/badge/timechimp)](https://pepy.tech/project/timechimp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
- TimeChimp endpoints are defined in `timechimp.api`

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

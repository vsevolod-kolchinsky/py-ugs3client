# UGS3 Python SDK

[![GitHub release](https://img.shields.io/github/release/vsevolod-kolchinsky/py-ugs3client.svg)]() [![Code Climate](https://codeclimate.com/github/vsevolod-kolchinsky/py-ugs3client/badges/gpa.svg)](https://codeclimate.com/github/vsevolod-kolchinsky/py-ugs3client)

[Bristar Studio](http://bristarstudio.com) Universinet Gaming Services Python client implementation.

## Installing

```
pip install py-ugs3client
```

## Usage

```python
from ugs3client import UGS3Client

ugs3 = UGS3Client()
containers = ugs3.find_containers(payload__type=1)

```

# UGS3 Python SDK

[![Documentation Status](https://readthedocs.org/projects/py-ugs3client/badge/?version=latest)](http://py-ugs3client.readthedocs.io/?badge=latest) [![GitHub release](https://img.shields.io/github/release/vsevolod-kolchinsky/py-ugs3client.svg)]() [![Code Climate](https://codeclimate.com/github/vsevolod-kolchinsky/py-ugs3client/badges/gpa.svg)](https://codeclimate.com/github/vsevolod-kolchinsky/py-ugs3client)

[Bristar Studio](http://bristarstudio.com) Universinet Gaming Services Python client implementation.

```
Copyright 2016 Vsevolod Kolchinsky

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

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

   

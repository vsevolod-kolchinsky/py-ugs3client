# UGS3 Python SDK

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
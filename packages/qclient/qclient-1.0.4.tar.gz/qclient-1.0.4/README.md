# qclient

## Install

```sh
pip install qclient
```

## Usage

> See test file for more examples

```python
import qclient

qclient.configure({'token': 'YOUR_TOKEN'})
print(qclient.get('bell'))
print(qclient.execute('bell'))
```
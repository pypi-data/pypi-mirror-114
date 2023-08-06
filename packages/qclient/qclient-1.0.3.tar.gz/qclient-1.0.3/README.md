# qclient

## Install

```sh
pip install qclient
```

## Usage

```python
import qclient
from sys import argv

#qclient.configure({ 'server': 'http://localhost:8080' })
token = 'YOUR_TOKEN' if len(argv) < 2 else argv[1]
qclient.configure({'token': token, 'server': 'http://localhost:8080'})

# [optional] display file to be executed
print(qclient.get('bell'))  # default extension
# print(qclient.get('bell.qasm')) # explicit extension

# execute and return
print('Executing...')
print(qclient.execute('bell'))
```
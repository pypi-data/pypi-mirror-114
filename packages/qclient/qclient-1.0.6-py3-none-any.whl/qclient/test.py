import qclient
from sys import argv

#qclient.configure({ 'server': 'http://localhost:8080' })
token = 'YOUR_TOKEN' if len(argv) < 2 else argv[1]
qclient.configure({'token': token, 'server': 'http://localhost:8080'})

# [optional] display file to be executed
print(qclient.get('bell'))  # default extension
# print(qclient.get('bell.qasm')) # explicit extension

# execute a previously stored algorithm
print('Executing...')
print(qclient.execute('bell'))

# execute a custom algorithm
data = '''
OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
measure q[0] -> c[0];
'''
print(qclient.execute(data))

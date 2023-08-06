from urllib import request, parse
import ssl

EXT = '.qasm'
ENDPOINT = 'https://quantum.tecnalia.com'
ENDPOINT_ALGORITHMS = ENDPOINT+'/algorithms'
ENDPOINT_SERVICES = ENDPOINT+'/services'
USER_TOKEN = 'YOUR_TOKEN'

ssl._create_default_https_context = ssl._create_unverified_context


def configure(options):
    '''
    Override default settings.

    {
        'server': the qserver address,
        'ext': the default extension for algorithms (.qasm, .quil, etc), 
        'token': authorization token to execute services
    }
    '''
    global EXT, ENDPOINT, ENDPOINT_ALGORITHMS, ENDPOINT_SERVICES, USER_TOKEN
    if 'ext' in options:
        EXT = options['ext']
    if 'server' in options:
        ENDPOINT = options['server']
        ENDPOINT_ALGORITHMS = ENDPOINT+'/algorithms'
        ENDPOINT_SERVICES = ENDPOINT+'/services'
    if 'token' in options:
        USER_TOKEN = options['token']


def get(name: str) -> str:
    '''Get the source text of the algorithm. Example: bell or bell.qasm or bell.quil'''
    realName = name if '.' in name else name + EXT
    req = request.Request(ENDPOINT_ALGORITHMS+'/'+realName)
    # req.add_header('Authorization', os.environ['TOKEN'])
    return request.urlopen(req).read().decode('utf-8')


def execute(name_or_data: str) -> str:
    '''
    Execute an algorithm

    If name -> Execute an existing algorithm from database
    If data -> Execute the algorithm described in data
    '''
    if len(name_or_data) < 20:
        realName = name_or_data if '.' in name_or_data else name_or_data + EXT
        data = ''.encode('utf-8')
        req = request.Request(ENDPOINT_SERVICES+'/run/' + realName, data)
        return request.urlopen(req).read().decode('utf-8')
    else:
        data = name_or_data.encode('utf-8')
        req = request.Request(ENDPOINT_SERVICES+'/run', data)
        return request.urlopen(req).read().decode('utf-8')

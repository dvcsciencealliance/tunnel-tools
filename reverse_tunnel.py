import subprocess
from pprint import pprint

import hjson

from checks import get_config

def main():
    config = get_config()
    
    subprocess.call(['killall', 'autossh'])

    tunnel = config['tunnel']
    url = tunnel['url']
    port = tunnel['port']
    remote_port = tunnel['remote_port']
    local_port = tunnel['local_port']
    key_file = tunnel['key_file']

    subprocess.call([
        'autossh',
        '-f', '-nNT',
        url,
        '-p', str(port),
        '-R', '*:{}:localhost:{}'.format(remote_port, local_port),
        '-i', key_file,
    ])

if __name__ == '__main__':
    main()

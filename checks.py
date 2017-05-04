
import os

from datetime import datetime
import urllib.request, urllib.error
import subprocess
from pprint import pprint

import requests
import hjson

def do_portal(username, password):
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'username': username, 'password': password}

    session = requests.Session()
    portal_url = 'https://portal.4cd.edu:9998/forms/user_login'
    res = session.post(portal_url, headers=headers, data=payload)
    print(res.text)

def internet_on(url, check_str):
    try:
        resp = urllib.request.urlopen(url, timeout=1)
        text = resp.read()
        if check_str.encode() not in text:
            return False
        return True
    except urllib.error.URLError as err:
        return False

def get_wpa_status():
    output = subprocess.check_output(["/sbin/wpa_cli", "status"])
    output = output.decode('utf8')
    output = output.split("\n")
    output = [o.split("=") for o in output if o and '=' in o]
    output = {k: v for k, v in output}
    #print(output)
    return output

def ensure(search_str, call_args):
    ps = subprocess.check_output(["ps", "aux"])
    ps = ps.decode('utf8')
    #print(ps)
    running = search_str in ps
    started = False
    start_failed = False
    
    if not running:
        call_args[1:] = (os.path.expanduser(p) for p in call_args[1:])
        res = subprocess.call(call_args)
        if res == 0:
            started = True
        else:
            start_failed = True
    
    return {
        'running': running,
        'started': started,
        'start_failed': start_failed,
    }

def get_config(config_path=None):
    if config_path is None:
        config_path = os.environ.get('TUNNEL_CONFIG', '~/tunnel/config.hjson')
        config_path = os.path.expanduser(config_path) #expand ~
    with open(config_path) as f:
        config = hjson.loads(f.read())
    return config

def main():
    print(datetime.now())
    config = get_config()
    #pprint(config)
    
    iok = internet_on(config['internet']['url'], config['internet']['str'])
    print("internet", iok)
    wpa_status = get_wpa_status()
    ssid = wpa_status.get('ssid')
    print("ssid", ssid)
    print("ip", wpa_status.get('ip_address'))
    
    if ssid in config['portal_ssids'] and not iok:
        try:
            auth = config['portal_auth']
            do_portal(auth['user'], auth['pass'])
        except requests.exceptions.ConnectionError as e:
            print("portal error:", e)
    
    for proc_name, proc in config['ensure'].items():
        print(proc_name)
        result = ensure(proc['ps'], proc['run'])
        for sr, status in result.items():
            if status:
                print(" ", sr)
    print()

if __name__ == "__main__":
    main()

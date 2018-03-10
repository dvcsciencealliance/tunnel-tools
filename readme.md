# Setup

```bash
git clone https://github.com/dvcsciencealliance/tunnel-tools.git ~/tunnel
mkdir ~/logs
virtualenv -p python3 ~/venv
source ~/venv/bin/activate
pip install -r ~/tunnel/requirments.txt
sudo apt-get install autossh
```

crontab

```crontab
@reboot ~/tunnel/run_reverse_tunnel.sh
@reboot ~/tunnel/run_digbot.sh

* * * * * ~/tunnel/run_checks.sh
```

create config files

# Config

### Config Files
* `config.hjson`
* `digbot/tunnel_config.hjson`
* `digbot/config.txt`

### Example Config Files Without SSH Tunnels

`config.hjson`
```hjson
internet: {
    url: http://google.com
    str: "<title>Google</title>"
}

portal_auth: {
    user: -
    pass: -
}

portal_ssids: [
    College-Students
]
```

### Example Config Files With SSH Tunnels
`config.hjson`
```hjson
internet: {
    url: http://google.com
    str: "<title>Google</title>"
}

portal_auth: {
    user: -
    pass: -
}

portal_ssids: [
    College-Students
]

ensure: {
    autossh: {
        ps: autossh
        run: [
            bash
            ~/tunnel/reverse_tunnel.sh
        ]
    }
    digbot: {
        ps: digbot
        run: [
            bash
            ~/tunnel/run_digbot.sh
        ]
    }
}

tunnel: {
    url: pi@host.com
    port: 22,
    remote_port: 2222
    local_port: 22
    key_file: ~/.ssh/id_rsa
}
```

`digbot/config.txt`
```
123456789:QWERTYUIOPASDFGHJKLZXCVBNMqw-ertyui
123456789, 12345678
123456789, 123467890
```

`digbot/tunnel_config.json`
```json
{
  "user":"pi",
  "addr":"host.com",
  "port":"22",
  "remote_port":"2223",
  "local_addr": "localhost",
  "local_port":"22",
  "key":"/home/pi/.ssh/id_rsa"
}
```

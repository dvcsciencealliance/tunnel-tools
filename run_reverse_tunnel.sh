#! /bin/bash

exec &>> ~/logs/reverse-tunnel-log.txt

source ~/venv/bin/activate

cd ~/tunnel
python reverse_tunnel.py

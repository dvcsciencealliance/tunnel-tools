#! /bin/bash

exec &>> ~/logs/checks-log.txt

cd ~/tunnel

source ~/venv/bin/activate

python checks.py

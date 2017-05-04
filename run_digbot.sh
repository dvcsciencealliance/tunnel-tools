#!/bin/bash

exec &>> ~/logs/digbot-log.txt

cd ~/tunnel/digbot

source ~/venv/bin/activate

# kill processes matching pattern
pkill -f "python tunbot.py"

python tunbot.py &

disown

#!/usr/bin/env sh

sed -n '/Start_keys/,/End_keys/p' ~/.config/qtile/config.py | grep -v '#End_' | grep -v '#Start_' | sed -e 's/Key /\n/' | sed -e 's/# /\n/' | yad --text-info --back=#282a36 --fore=#f8f8f2 --geometry=800x500:

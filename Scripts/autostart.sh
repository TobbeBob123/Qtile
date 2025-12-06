#!/usr/bin/env sh

~/.fehbg &
picom --backend xrender &
lxsession &
dbus-update-activation-environment --systemd DISPLAY eval $(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh) export SSH_AUTH_SOCK &
dunst &
nm-applet &
signal-desktop &
~/Script/husk_oppdater.sh &
blueman-applet &
/usr/bin/emacs --daemon &
discord &
autolock -time 30 -locker -corners ++-- 'systemctl suspend' &
setxkbmap -option caps:swapescape &

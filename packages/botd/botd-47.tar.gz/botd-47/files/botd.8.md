% BOTD(8) BOTD(8)
% Bart Thate
% Aug 2021

# NAME
BOTD - 24/7 channel daemon

# SYNOPSIS
sudo botctl \<cmd\>

# DESCRIPTION
BOTD is a pure python3 IRC chat bot that can run as a background
daemon for 24/7 a day presence in a IRC channel. You can install
it as a service so it restarts on reboot. It can be used to
display RSS feeds, act as a UDP to IRC relay and you can program
your own commands for it. 

# CONFIGURATION
| cp /usr/local/share/botd/botd.service /etc/systemd/system
| systemctl enable botd
| systemctl daemon-reload
| systemctl restart botd

# SEE ALSO
| bot
| botcmd
| botctl
| /var/lib/botd
| /var/lib/botd/mod
| /usr/local/share/botd/botd.service

# COPYRIGHT
BOTD is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

# AUTHOR
Bart Thate \<bthate67@gmail.com\>

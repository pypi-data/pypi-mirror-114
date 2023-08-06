% BOT(1) BOT(1)
% Bart Thate
% Aug 2021

# NAME
BOT - python3 irc bot

# SYNOPSIS
| bot \<cmd>\ 
| bot cfg server=irc.freenode.net channel=\\#botd
| bot m=bot.irc,bot.rss

# DESCRIPTION
BOT is the user client version of BOTD, it can be used in development of bot
commands. Uses ~/.bot as the work directory.

# EXAMPLES

| $ bot
| $ 

| $ bot cmd
| cfg,cmd,dlt,ech,exc,flt,fnd,krn,met,sve,thr,upt,ver

| $ bot cfg
| cc=@ channel=#botd nick=botd port=6667 server=localhost

| bot krn
| $ cmd=krn name=bot txt=krn users=True version=1 wd=/home/bart/.bot

| $ bot thr
| CLI.handler 0s | CLI.input 0s

| $ bot m=bot.irc,bot.rss
| >

# SEE ALSO
| botd
| botctl
| ~/.bot
| ./mod

# COPYRIGHT
BOT is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

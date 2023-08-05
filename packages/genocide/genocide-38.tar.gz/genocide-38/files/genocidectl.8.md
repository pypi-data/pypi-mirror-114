% GENOCIDECTL(8)  GENOCIDECTL(8)
% Bart Thate
% April 2021

# NAME
GENOCIDECTL - control the genocide daemon

# SYNOPSIS
sudo genocidectl \<cmd\>

# DESCRIPTION
GENOCIDECTL executes genocidecmd under the systemd-exec wrapper, this to make
commands run under systemd. Uses /var/lib/genocide as the work directory and
/vae/lib/botd/mod as the modules directory.

# EXAMPLES
| sudo genocidectl cmd
| sudo genocidectl cfg server=irc.freenode.net channel=\#dunkbots nick=genocide
| sudo genocidectl met ~botfather@jsonbot/daddy
| sudo genocidectl rss https://github.com/bthate/genocide/commits/master.atom
| sudo genocidectl krn mods=rss

# AUTHOR
Bart Thate \<bthate67@gmail.com\>

# COPYRIGHT
GENOCIDECTL is placed in the Public Domain and contains no Copyright and no LICENSE.

# SEE ALSO
| genocide
| genocided
| /var/lib/genocide
| /usr/local/share/genocide/genocide.service

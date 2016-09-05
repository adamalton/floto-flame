# Installation

The things (as best as I can remember) that I did in order to get this up and running on the Raspberry Pi.

1. Install Raspian.
1. At the boot menu, change password, switch on SSH access, switch to desktop boot mode.
1. Install `easy_install` (in order to install `pip`).
1. `pip install virtualenv`.
1. `virtualenv photoframe_env`.
1. `cd photoframe_env; git clone <this repo>`.
1. Install Iceweasel (using `sudo apt-get update; sudo apt-get upgrade; sudo apt-get install Iceweasel`).
1. Prevent screen blanking by editing `/etc/kbd/config` and setting `BLANK_TIME=0` and `POWERDOWN_TIME=0`, and also editing `/etc/lightdm/lightdm.conf` and after the line `[SeatDefaults]` adding `xserver-command=X -s 0 dpms`.
1. Add the `keep_running_cron.sh` script to the cron with `crontab -e`, setting it as per below \[1].


\[1]
```
@reboot                                 /home/pi/photoframe_env/floto-flame/ssh/keep_running_cron.sh
*/5     *       *       *       *       /home/pi/photoframe_env/floto-flame/ssh/keep_running_cron.sh
```

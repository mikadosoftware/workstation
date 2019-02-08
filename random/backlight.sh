#Turning on the Backlight for my Dell laptop keyboard
#####################################################
#I often am coding in a dark coach on my commute, so having my keyboard backlight
#working is very useful.  How on earth I ever found this directory I cannot remember,
#but it is useful - and part of replicating my workstation (at least on a Dell laptop!)
#
#/sys/devices/platform/dell-laptop/leds/dell::kbd_backlight

#I set the brightness file to 2 (0 was off, 3 is max) and
# I set the stop-timeout to be 120m (from 1 m)


### Run as sudo from command line, after system updates.
DIR=/sys/devices/platform/dell-laptop/leds/dell\:\:kbd_backlight/
echo 2 > $DIR\brightness
echo 120m > $DIR\stop-timeout

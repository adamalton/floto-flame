# Cron script to check that the photo frame server is still running and that the browser is still open

cd /home/pi/photoframe_env/floto-flame/ssh


# Make sure that the Raspberry Pi's screen saver / screen blanking is disabled.
# Note that other system settings are needed as well as this
./prevent_screen_saver.sh


# First check that the server is running

num_runserver_processes=$( ps ax | grep "runserver" | wc -l )
# The ps/grep command itself gets included, so 1 process == 0
if [ $num_runserver_processes -eq 1 ]
then
    ./start_server.sh
fi


# Now sleep for a little while to make sure that we give it time to start up
sleep 5


# Now make sure that the broswer is up and running
num_iceweasel_processes=$( ps ax | grep "iceweasel" | wc -l )
# The ps/grep command itself gets included, so 1 process == 0
if [ $num_iceweasel_processes -eq 1 ]
then
    ./open_browser.sh
fi

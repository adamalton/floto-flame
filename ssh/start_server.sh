# TODO: don't hard code the photo frame folder location and/or use Apache instead
cd ~/photoframe_env
source bin/activate
cd floto-flame
# By specifying 0.0.0.0 we allow it to accept incoming network connections from other devices
# on the same network, i.e. it allows me to access /shutdown/ from my phone on my home wifi
nohup python manage.py runserver 0.0.0.0:8000 &

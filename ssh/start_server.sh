# TODO: don't hard code the photo frame folder location and/or use Apache instead
cd ~/photoframe_env
source bin/activate
cd floto-flame
nohup python manage.py runserver &
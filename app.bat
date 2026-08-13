call env\scripts\activate.bat
cls
ipconfig
title YB IT SOLUTIONS: MCRO VERIFICATION SYSTEM
python manage.py runserver 0.0.0.0:8000
pause

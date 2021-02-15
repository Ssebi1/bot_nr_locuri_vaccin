@ECHO OFF
pip install virtualenv
virtualenv sendsms
pip install twilio
pip install requests
pip install beautifulsoup4
pip install python-decouple
ECHO Bot starting
python bot.py

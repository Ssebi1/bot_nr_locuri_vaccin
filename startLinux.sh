#!/bin/bash
pip install virtualenv
virtualenv sendsms
source sendsms/bin/activate
pip install beautifulsoup4
pip install twilio
pip install requests
pip install python-decouple
echo "Bot is starting"
python bot.py

from time import sleep
import time;
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
from decouple import config
from decouple import Csv

# Alternatively without .env:  
# client = Client(INSERT TWILIO CLIENT USERNAME,INSERT TWILIO CLIENT KEY))
client = Client(config("TWILIO_CLIENT_USERNAME"),config("TWILIO_CLIENT_KEY"))


# Functions
def send_message(numere,from_number,body):
    for numar in numere:
        client.messages.create(to=numar, from_=from_number, body=body)


def get_data(timestamp):
    url = 'https://vaccinare-covid.gov.ro/wp-content/themes/twentytwenty/assets/map/nr_loc_center.json?v='+str(timestamp)
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    soup = soup.prettify()
    return soup


def compute_free(data):
    total_locuri = 0
    for id in id_centre:
        index = data.find(id)
        if index:
            nr_locuri_libere = 0
            for c in data[index+20:index+28]:
                if c>='0' and c<='9':
                    nr_locuri_libere = nr_locuri_libere*10 + (int)(ord(c)-ord('0'))
            total_locuri += nr_locuri_libere
    
    return total_locuri


def compute_history(time,value):
    print(time,': ',value,sep='')
    g.write(str(time)+': '+str(value)+'\n')


# Data


# Alternatively without .env:  
# id_centre = ['202222','20333','204444']
id_centre = config('CENTRE',cast=Csv())

# Alternatively without .env:  
# numere_telefon = ['+444444444444'.'+44433333333']
numere_telefon = config('NUMBERS',cast=Csv())

refreshRate = 60
twilio_number = config("TWILIO_NUMBER")
gasit = False
g = open('history.txt','a');


while True:
    timestamp = int(time.time())
    data = get_data(timestamp)
    total_locuri = compute_free(data)
    dt = datetime.fromtimestamp(timestamp)
    compute_history(dt,str(total_locuri))

    if gasit==False and total_locuri>0:
        send_message(numere_telefon,twilio_number,"Numar locuri libere: {}".format(total_locuri))
        gasit = True

    sleep(refreshRate)
    

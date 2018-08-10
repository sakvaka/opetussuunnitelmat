# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone, date
import icalendar
import urllib.request
from dateutil.rrule import *
from operator import itemgetter

# luettelo ohjelmista
ohjelmat = {
	"926" : ("Alkeishiukkasfysiikka ja astrofysikaaliset tieteet (FM)"),
	"932" : ("Datatiede (FM)"),
	"924" : ("Elämäntieteiden informatiikka (FM)"),
	"933" : ("Geologia ja geofysiikka (FM)"),
	"928" : ("Ilmakehätieteet (FM)"),
	"935" : ("Kaupunkitutkimus ja -suunnittelu (FM)"),
	"929" : ("Kemia ja molekyylitieteet (FM)"),
	"934" : ("Maantiede (FM)"),
	"923" : ("Matematiikka ja tilastotiede (FM)"),
	"930" : ("MFK-ope (FM)"),
	"927" : ("Materiaalitutkimus (FM)"),
	"925" : ("Teoreettiset ja laskennalliset menetelmät (FM)"),
	"931" : ("Tietojenkäsittelytiede (FM)"),
	"917" : ("Fysikaaliset tieteet (LuK)"),
	"921" : ("Geotieteet (LuK)"),
	"918" : ("Kemia (LuK)"),
	"922" : ("Maantiede (LuK)"),
	"916" : ("Matemaattiset tieteet (LuK)"),
	"919" : ("MFK-ope (LuK)"),
	"920" : ("Tietojenkäsittelytiede (LuK)")
}

# tulosta ohjelmat ja niiden koodit
for key, value in ohjelmat.items():
    print(key, " - ", value)

valittu = input('Valitse koulutusohjelma: ')

print('Haetaan koulutusohjelman kursseja...')
icalfile = urllib.request.urlopen('https://future.optime.helsinki.fi/icalservice/Department/'+valittu)
gcal = icalendar.Calendar.from_ical(icalfile.read())

muisti=[0,0]

# kiellettyjä sanoja
blacklisted = ['harjoitu', 'övning', 'labra', 'ex tempore', 'exerci', 'excerci', 'Itsenäinen', 'paja', 'Kisälliohjau', 'kokoukset', 'seminar', 'seminaar']
uusilista=[]

print()
print('=== KURSSILISTAUS ===')
print('Huom! Ei sisällä kursseja, jotka alkavat opetustauoilla (esim. intensiivikurssit). Ei myöskään sisällä laskuharjoitusryhmiä, seminaareja, ot-ryhmiä tai pajoja.')
print('Huom! Viikonpäivät 0-4 tarkoittaa ma-pe.')
print()

for component in gcal.walk():
      if component.name == "VEVENT" and not any(x in component.to_ical().decode("utf-8") for x in blacklisted):
        summary = component.get('summary')
        description = component.get('description')
        location = component.get('location')
        startdt = component.get('dtstart').dt
        enddt = component.get('dtend').dt
        exdate = component.get('exdate')
        weekday= startdt.weekday()
        starttime= startdt.hour*100+startdt.minute
        
        if startdt >= datetime(2018,9,3) and startdt <= datetime(2018,10,21):
            periodi=1
        elif startdt >= datetime(2018,10,29) and startdt <= datetime(2018,12,16)                                                                                        :
            periodi=2
        elif startdt >= datetime(2019,1,14) and startdt <= datetime(2019,3,3):
            periodi=3
        elif startdt >= datetime(2019,3,11) and startdt <= datetime(2019,5,5):
            periodi=4
        else:
            continue
        if (muisti[0] != weekday or muisti[1] != starttime):
            uusilista.append((periodi,weekday,startdt.strftime("%H:%M"), summary, description, location))
        muisti[0]=weekday
        muisti[1]=starttime

# laitetaan periodin, päivän ja kellonajan mukaiseen järjestykseen
uusilista.sort(key=itemgetter(0,1,2))

for alkio in uusilista:
    print("Periodi #{0}: päivä {1}: klo {2} : {3} {4} {5}\n".format(alkio[0],alkio[1],alkio[2], alkio[3], alkio[4], alkio[5]))

icalfile.close()

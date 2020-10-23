#!/usr/bin/python2.7

import urllib2, serial, feedparser, time

SERIALPORT = "/dev/tty.usbmodemfd121" # Serieller Port (Bitte anpassen)

# Seriellen Port konfigurieren
try:
    ser = serial.Serial(SERIALPORT, 9600)
except serial.SerialException:
    sys.exit()

auth_handler = urllib2.HTTPBasicAuthHandler()

#Hier die Zugangsdaten zum GMail-Account eintragen
auth_handler.add_password('New mail feed', 'https://mail.google.com/','BENUTZERNAME', 'PASSWORT')

opener = urllib2.build_opener(auth_handler)
feed_file = opener.open('https://mail.google.com/mail/feed/atom/')

# Feed mit feedparser parsen
d = feedparser.parse(feed_file)

#Anzahl der ungelesenen Gmails
newmails = d.feed.fullcount

# Senden der Anzahl der ungelesenen
# Gmails ueber den seriellen Port
if newmails > 0:
  ser.write(str(newmails))
  time.sleep(1)

# Anzahl der Gmails, Betreff und Autor im Terminal ausgeben
  print 'Anzahl Gmails:', d.feed.fullcount
  for entry in d.entries:
    print '----------------------------------------------'
    print 'Author: ', entry.author
    print 'Betreff:', entry.title
else:
  ser.write(0)
  time.sleep(1)

# seriellen Port schliessen
ser.close()
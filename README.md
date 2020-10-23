# Cordwood-Puzzle-Gmail-Anzeige

Mar 7th, 2014

Diese Anleitung zeigt den Aufbau einer Benachrichtigungsanzeige für Gmail aus folgenden Komponenten:

- Cordwood Puzzle von Boldport

- Arduino (beliebig)

![CordwoodPuzzle von Boldport](https://github.com/felixfreyer/Cordwood-Puzzle-Gmail-Anzeige/raw/main/notifier0.jpg "CordwoodPuzzle von Boldport")
<br />
**Abbildung 1: CordwoodPuzzle von Boldport**

Die sechs LEDs werden über separate Pins vom Arduino gesteuert. Für den Einsatz als Gmail-Anzeige wird eine einfache Ampelschaltung vorgesehen.

**Arduino Firmware:**

```c
/*
  GetGMail
  Dieses Sketch wartet auf ankommende Signale überd en seriellen Port
  Wird ein M empfangen dann fängt eine RGB LED an im Takt zu blinken und
  dabei ihre Farbe zu ändern. Wenn ein N empfangen wird, dann wird die LED 
  abgeschaltet.
 
  Zu diesem Script gehört das Python-Script check-gmail.py das minütlich durch einen
  CronJob aufgerufen wird. Das Python-Script  verbindet sich zum Google-Mail-Server und
  fragt ab ob ungelesene eMails im Posteingang sind. Je nach Wert wird ein M oder ein N 
  an der seriellen Port gesendet. 
*/

int greenled_1 = A13; // Led's and pins
int yellowled_1 = A14;
int redled_1 = A15;
int greenled_2 = A12;
int yellowled_2 = A11;
int redled_2 = A10;

int val      = 0;        // Wert aus dem seriellen Anschluss zu lesen
int DELAY    = 200;      // Intervall zwischen Wechsel der Farben

void setup ()
{
  // Init Led's
  pinMode(greenled_1, OUTPUT);
  pinMode(yellowled_1, OUTPUT);
  pinMode(redled_1, OUTPUT);
  pinMode(greenled_2, OUTPUT);
  pinMode(yellowled_2, OUTPUT);
  pinMode(redled_2, OUTPUT);
  digitalWrite(greenled_1, LOW);
  digitalWrite(greenled_2, LOW);
  digitalWrite(yellowled_1, LOW);
  digitalWrite(yellowled_2, LOW);
  digitalWrite(redled_1, LOW);
  digitalWrite(redled_2, LOW);

  Serial.begin (9600);
  Serial.flush ();
}

void loop ()
{
  getNewMails(DELAY);
}

void getNewMails(int Pause)
{
  while(int i=-1)
  {
    if (Serial.available())
    val = Serial.read()-48;

    if (val > 0)
    {
      Serial.println("eMails: "+String(val));
      digitalWrite(greenled_1, HIGH);   // Green on
      digitalWrite(greenled_2, HIGH);
      digitalWrite(redled_1, LOW);      // Red off
      digitalWrite(redled_2, LOW);
      delay(Pause);
      digitalWrite(greenled_1, LOW);    // Green off
      digitalWrite(greenled_2, LOW);    
      digitalWrite(yellowled_1, HIGH);  // Yellow on
      digitalWrite(yellowled_2, HIGH);
      delay(Pause);
      digitalWrite(redled_1, HIGH);     // Red on
      digitalWrite(redled_2, HIGH);
      digitalWrite(yellowled_1, LOW);   // Yellow off
      digitalWrite(yellowled_2, LOW);
      delay(Pause);
    }
    else
    {
      digitalWrite(greenled_1, LOW);  // Green off
      digitalWrite(greenled_2, LOW);
      digitalWrite(yellowled_1, LOW); // Yellow off
      digitalWrite(yellowled_2, LOW);
      digitalWrite(redled_1, LOW);    // Red off
      digitalWrite(redled_2, LOW);
    }
  }
}
```

Nach der Programmierung kann der Arduino an den PC angeschlossen und das Python-Skript zur Gmail-Abfrage ausgeführt werden.

![CordwoodPuzzle von Boldport](https://github.com/felixfreyer/Cordwood-Puzzle-Gmail-Anzeige/raw/main/notifier1.jpg "Gmail-Anzeige mit CordwoodPuzzle")
<br />
**Abbildung 2: Gmail-Anzeige mit CordwoodPuzzle**
<br />

**Python-Skript für Gmail-Abruf:**

```python
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
```

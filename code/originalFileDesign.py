import os
import time
import bluetooth
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
from random import *

GPIO.setmode(GPIO.BCM)

# Setup the button

buttonBookPin = 20;
buttonPCPin = 25;
GPIO.setup(buttonBookPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(buttonPCPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

bd_addr = "98:D3:31:F5:22:E7"
# Raspberry Pi pin configuration:
lcd_rs        = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11

 
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)
counter=0
port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))


def firstButtonPress():
    relayState = False
    lcd.clear()
    lcd.message(' Please Choose: \nBook        PC')
    try:
        while not relayState:
        
            if GPIO.input(buttonBookPin):
                print("book")
                relayState=True
            if GPIO.input(buttonPCPin):
                print("pc") 
                relayState=True            
            
            time.sleep(1)    
    finally:
        lcd.clear()
        lcd.message('Loading...')
        time.sleep(1)
        
def checkDist():
    dist=(sock.recv(1024))
    print(dist)
    if dist=='c':
        lcd.clear()
        lcd.message('Please move back')
        execfile('/home/pi/Desktop/tooclose.py')
        
        while dist == "c":
            time.sleep(1)
            dist=(sock.recv(1024))
            print(dist+'stuck')
              
    if dist=="n":
        time.sleep(1)
    if dist=="f":
        time.sleep(1)
def checkFarDist():
    dist=(sock.recv(1024))
    time.sleep(1)
    dist=(sock.recv(1024))
    print(dist)
    if dist=='f':
        return False
    else:
        return True
def checkButtonReset():
    if GPIO.input(buttonBookPin):
        lcd.clear()
        lcd.message('Loading...')
        time.sleep(2)
        firstButtonPress()
        global counter
        counter=0
def checkButtonCounter():
    if GPIO.input(buttonPCPin):
        lcd.clear()
        lcd.message('Loading...')
        global counter
        counter=1199#set to correct
        time.sleep(1)
def checkCounter():
    global counter
    if counter==1200:#change accordingly
        lcd.clear()
        lcd.message('Take a Break')
        execfile('/home/pi/Desktop/servo.py')#change accordingly
        time.sleep(9)
        execfile('/home/pi/Desktop/servo.py')
        Persistent=checkFarDist()
        if Persistent:
            execfile('/home/pi/Desktop/fade_in_out_rmb_change_gpio.py')#change accordingly
            time.sleep(10)
        Persistent=checkFarDist()
        if Persistent:
            execfile("/home/pi/Desktop/mp3/takeabreak.py") #change accordingly           
            while Persistent:
                time.sleep(1)
                Persistent=checkFarDist()
                print(Persistent)
        choice=randint(1,3)
        if choice == 1:
            execfile("/home/pi/Desktop/mp3/edsheeran.py")       #change accordingly
            time.sleep(31)
        elif choice == 2:
            execfile("/home/pi/Desktop/mp3/yiruma.py")
            time.sleep(49)
        elif choice == 3:
            execfile("/home/pi/Desktop/mp3/maybe.py")
            time.sleep(33)
        counter=0
def setCounterToLCD():
    global counter
    rawCounter=int(counter/60)
    rawCounter=20-rawCounter
    if rawCounter==0:
        rawCounter=1
    rawCounter=str(rawCounter)
    lcd.clear()
    lcd.message(rawCounter + ' minutes \nto next break')
def silentPlay():
    global counter
    if  not counter%50:
        execfile('/home/pi/Desktop/mp3/silent.py')#silent.mp3
        print('silent')
def main():
    
    firstButtonPress()#rmb to include lcd display
    try:
        while True:
            global counter
            checkDist()#senddata can be here, and also warning if too close, loop stays here
            checkButtonReset()#need timesleep and first button press here
            checkButtonCounter()#for set to counter 20
            checkCounter()# needs send data here, and music, and lamp(dim bright), alot of code here, smell, along with check dist(), along with relax(lamp colors)
            counter=counter+1
            setCounterToLCD()
            silentPlay()
    except Exception as e:
        print('error')
        print(e)
        sock.close()

main()

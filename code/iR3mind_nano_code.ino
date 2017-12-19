// Watch video here: https://www.youtube.com/watch?v=mkUbpeKAu24

/* HC-SR04 or RB URF02
 VCC to Arduino 5V 
 GND to Arduino GND
 Echo (or OUTPUT) to Arduino pin 2 
 Trig (or INPUT) to Arduino pin 3 */
#define echoPin 2 // Echo Pin (OUTPUT pin in RB URF02)
#define trigPin 3 // Trigger Pin (INPUT pin in RB URF02)
#include <VarSpeedServo.h>
#include "Wire.h"
#include <SPI.h>

VarSpeedServo myservo1;
VarSpeedServo myservo2;
int led = 6;
int maximumRange = 350; // Maximum range needed
int minimumRange = 0; // Minimum range needed
long duration, distance; // Duration used to calculate distance
int brightness;

void setup() {
 Serial.begin (9600);
 pinMode(trigPin, OUTPUT);
 pinMode(echoPin, INPUT);
 pinMode(led, OUTPUT);
  myservo1.attach(18);
   myservo2.attach(17); 
}

void loop() {
// The following trigPin/echoPin cycle is used to determine the distance of the nearest object by bouncing soundwaves off of it.
 digitalWrite(trigPin, LOW); 
 delayMicroseconds(2); 
 digitalWrite(trigPin, HIGH);
 delayMicroseconds(10); 
 digitalWrite(trigPin, LOW);
 duration = pulseIn(echoPin, HIGH);
 distance = duration/58.2; //Calculate the distance (in cm) based on the speed of sound.
 Serial.println(distance); // distance in cm
 delay(1000); //Delay 50 ms
  if (distance<=15)
  {myservo1.write(179,70,false); 
   myservo2.write(179,70,true);
   delay(500);
  
   myservo1.write(0,70,true); 
   delay(100);
   myservo2.write(0,70,true);
   delay(100);}
}

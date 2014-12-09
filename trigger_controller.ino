#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // twelve servo objects can be created on most boards
 
int pos = 0;    // variable to store the servo position 
int fire = 0; //
int hold = 0;
int trig = 1;
void setup() 
{ 
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
  //myservo.write(90);
} 
 void trigger(){
  myservo.write(0);
 delay(700);
myservo.write(180);
delay(500);
myservo.write(90);
calibrate(2);
calibrate(2);
Serial.println("I dont hate you");
 }
 void calibrate(int in){
   if( in == 1){
    myservo.write(180);
   delay(100);
  myservo.write(90); 
   }else if(in ==2){
   myservo.write(0);
   delay(100);
   myservo.write(90);
   }else{
   Serial.println("fail2");
 }
 }
 
void loop() { 
  myservo.write(90);
  while(!fire){
if(Serial.available() > 0){
    hold = Serial.read();
    trig = 1;
    if(hold == 102){
      fire = 1;
      trig = 0;
    }  
      else if(hold == 100){
        calibrate(1);
        trig = 0;
        }
    else if(hold == 97){
      calibrate(2);
      trig = 0;
    }
 
    }
  
  }
  trigger();
  fire = 0;
  } 

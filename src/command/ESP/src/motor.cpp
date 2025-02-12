#include "motor.h"


  // Constructor : 
Motor::Motor (int relay, Servo esc, int driver) {
    this->relay = relay;
    this -> driver = driver;
    this->esc = esc;
  }
  // Update the direction of the servo motors :
  void Motor::updateDirection (float y){
    // we only consider y for the  direction 
    if(y<0){
      digitalWrite(relay,HIGH);
    }
    else{
      digitalWrite(relay,LOW);
    }
  }

  void Motor::setSpeed(int speed){
    analogWrite(driver,speed);
  }

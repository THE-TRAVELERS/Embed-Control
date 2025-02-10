#include "motor.h"


  // Constructor : 
Motor::Motor (int relaisRight, int relaisLeft, Servo esc, Servo esc2, int RigthDriver, int LeftDriver) {
    this->relayRight = relaisRight;
    this->relayLeft = relaisLeft;
    this-> RigthDriver = RigthDriver;
    this -> LeftDriver = LeftDriver;
    this->esc = esc;
    this->esc2 = esc2;
  }
  // Update the direction of the servo motors :
  void Motor::updateDirection (float y){
    // we only consider y for the  direction 
    if(y<0){
      digitalWrite(relayRight,HIGH);
      digitalWrite(relayLeft,HIGH);
    }
    else{
      digitalWrite(relayRight,LOW);
      digitalWrite(relayLeft,LOW);
    }
  }

  void Motor::setSpeed(int left, int rigth){
    digitalWrite(RigthDriver,rigth);
    digitalWrite(LeftDriver,left);
  }

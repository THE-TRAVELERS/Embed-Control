#include "motor.h"


  // Constructor : 
Motor::Motor (int relaisRight, int relaisLeft, Servo esc, Servo esc2) {
    this->relayRight = relaisRight;
    this->relayLeft = relaisLeft;
    this->esc = esc;
    this->esc2 = esc2;
  }
  // Update the direction of the servo motors :
  void Motor::updateDirection (){
    // we only consider y for the  direction 
    if(ySign<0){
      digitalWrite(relayRight,HIGH);
      digitalWrite(relayLeft,HIGH);
    }
    else{
      digitalWrite(relayRight,LOW);
      digitalWrite(relayLeft,LOW);
    }
  }
  // function to convert receive float to sign 8 bytes float 
  void Motor::convert_unsign(float x, float y){
    ySign = (float)sqrt(y*y)*255;// absolute value to have 0 255 positive
    Serial.print("Unsign y : ");
    Serial.println(ySign);
    xSign = sqrt(x*x)*255; // absolute value to have 0 255 positive
    Serial.print("Unsign x : ");
    Serial.println(xSign);
  }

  // function to convert the received float to unsigned 8 bytes float
  void Motor::convert_sign(float x, float y){
    // convert the y value : 
    // -1 1 
    // -127 128
    // 0 255 
    ySign = (float)y*127/128;
    Serial.print("Sign y : ");
    Serial.println(ySign);
    
    xSign = (float)x*127/128;
    Serial.print("Sign x : ");
    Serial.println(xSign);

    // make the intensity on unsigned
    convert_unsign(xSign,ySign);
  }
  /*
  void Motor::stringToFloat(int len){
    // convert the string to float :
    for(int j=0; j<len; j++){
        temp[j] = Wire.read();
    }
    char* separator = strchr(temp,',');
    if(separator!=0){
        float a = atof(temp);
      	float b = atof(separator+1);
    }
  }
  */

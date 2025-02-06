#include "navigation.h"

// constructor 
Navigation::Navigation (Motor* Left_Motor, Motor* Right_Motor){
    this -> Left_Motor = Left_Motor;
    this -> Right_Motor = Right_Motor;
    this -> xCoordinate = 0; 
    this -> yCoordinate = 0;
    this -> xJoystick = 0; 
    this -> yJoystick = 0;
}

void Navigation::Joystick_sign (float x, float y){
    yJoystick = (float)y*127/128;
    Serial.print("Sign y : ");
    Serial.println(yJoystick);
    
    xJoystick = (float)x*127/128;
    Serial.print("Sign x : ");
    Serial.println(xJoystick);
}

void Navigation::Joystick_unsign(float x, float y){
    yJoystick = (float)sqrt(y*y)*255;// absolute value to have 0 255 positive
    Serial.print("Unsign y : ");
    Serial.println(yJoystick);

    xJoystick = sqrt(x*x)*255; // absolute value to have 0 255 positive
    Serial.print("Unsign x : ");
    Serial.println(xJoystick);
}

// TODO : Make the convert coordinates to indicates the direction of the robot

// TODO : Make the convert coordinates to indicates the direction of the robot
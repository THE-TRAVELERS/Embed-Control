#include "navigation.h"

// constructor 
Navigation::Navigation (Motor* Left_Motor, Motor* Right_Motorn, char *temp){
    this -> Left_Motor = Left_Motor;
    this -> Right_Motor = Right_Motor;
    this -> xCoordinate = 0; 
    this -> yCoordinate = 0;
    this -> xJoystick = 0; 
    this -> yJoystick = 0;
    this -> message  = temp;
    this -> Rightspeed = 0;
    this -> Leftspeed = 0;
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

void Navigation::Compute_Speed(){
    // TODO : make math to have the rigth speed for each motor
    int a = 4;
}


void Navigation::Joystick_command_direction(){
    // we ensure the rigth direction of the motors
    Left_Motor->updateDirection(yJoystick);
    Right_Motor->updateDirection(yJoystick);
    //now we send the unsign value to control the speed;
}


// TODO : Make the convert coordinates to indicates the direction of the robot

// TODO : Make the convert coordinates to indicates the direction of the robot
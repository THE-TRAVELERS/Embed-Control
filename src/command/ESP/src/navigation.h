#include "motor.h"


class Navigation{

private:
    // We use pointer to Motor class to access its methods
    Motor* Left_Motor;
    Motor* Right_Motor;
    
    float xCoordinate;
    float yCoordinate;

    float xJoystick;
    float yJoystick;    

public:
    // constructor
    Navigation(Motor* Left_Motor, Motor* Right_Motor);
    // convert the joystick values to sign float 
    void Joystick_sign(float x, float y);
    // convert the joystick values to sign float   
    void Joystick_unsign(float x, float y);

    // TODO : Make the convert coordinates to indicates the direction of the robot

    // TODO : Make the convert coordinates to indicates the direction of the robot
};
#include <Arduino.h>
#include <Wire.h>
#include <ESP32Servo.h>


class Motor {
    private: 
    // the ESC objects
    Servo esc;
    Servo esc2;

    // the value of the joystick
    float xSign;
    float ySign;

    // the relay pins 
    int relayRight;
    int relayLeft;

    // the speed of the motors
    float rightSpeed;
    float leftSpeed;


    public : 
    Motor();
    // constructor 
    Motor(int relayRight, int relayLeft, Servo esc, Servo esc2);

    // Update the direction of the servo motors : 
    void updateDirection();

    // convert 2 received float into sign float
    void convert_sign(float x, float y);

    void convert_unsign(float x, float y);

    void setSpeed();

    //TODO  : make the feedback about the speed of the motor 
    

    // TODO : make the feedback about the speed of the motor 
};
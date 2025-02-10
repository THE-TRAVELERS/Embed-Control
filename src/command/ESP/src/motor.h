#include <Arduino.h>
#include <Wire.h>
#include <ESP32Servo.h>
#ifndef motor.h
#define motor.h

class Motor {
    private: 
    // the ESC objects
    Servo esc;
    Servo esc2;

    // the relay pins 
    int relayRight;
    int relayLeft;

    int RigthDriver;
    int LeftDriver;


    public : 
    Motor();
    // constructor 
    Motor(int relayRight, int relayLeft, Servo esc, Servo esc2, int RigthDriver, int LeftDriver);

    // Update the direction of the servo motors : 
    void updateDirection(float y);

    void setSpeed(int left, int rigth);


    //TODO  : make the feedback about the speed of the motor 
    

    // TODO : make the feedback about the speed of the motor 
};


#endif
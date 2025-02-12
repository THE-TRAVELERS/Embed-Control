#include <Arduino.h>
#include <Wire.h>
#include <ESP32Servo.h>
#ifndef motor.h
#define motor.h

class Motor {
    private: 
    // the ESC objects
    Servo esc;

    // the relay pins 
    int relay;

    int driver;


    public : 
    Motor();
    // constructor 
    Motor(int relay, Servo esc, int driver);

    // Update the direction of the servo motors : 
    void updateDirection(float y);

    void setSpeed(int speed);


    //TODO  : make the feedback about the speed of the motor 
    

    // TODO : make the feedback about the speed of the motor 
};


#endif
/*
  TRAVELERS version DELTA 
  
  Basé sur le code de controle COSTE@2024 et réception I2C TOURON@2022

  Ce programme contrôle un microcontrôleur ESP32 qui interfère avec deux ESCs 
  (Electronic Speed Controllers) et des moteurs via la communication I2C.
*/
#include <Arduino.h>
#include <Wire.h>
#include <ESP32Servo.h>

// I2C address of the esp
#define I2C_DEV_ADDR 0x52
int relaisRight =1;
int relaisLeft=2;

// Servo object to control the ESC
Servo esc;
Servo esc2;

// I2C received flag 
volatile boolean receiveFlag = false; // Drapeau pour la réception de données I2C


// I2C received data
char temp[32]; 

// joystick position : 
float x;
float y;

//Function for reading the received data
void onReceive(int len){
  // TODO : Make different case for different input values 
  for(int j=0; j<len; j++){
      temp[j] = Wire.read();
  }
  char* separator = strchr(temp,',');
  if(separator!=0){
      x = atof(temp);
      y = atof(separator+1);
  }
// TODO : Make different case for different input values 
  receiveFlag = true;
}

void setup(){
    Wire.onReceive(onReceive);
    Wire.begin((uint8_t)I2C_DEV_ADDR);
    Serial.begin(9600);


  	// setup the servo pinmode

  
  	// setup the relais pins mode
  	pinMode(relaisRight,OUTPUT);
  	pinMode(relaisLeft,OUTPUT);
  
  	// write to go in front 
  	digitalWrite(relaisRight,LOW);
  	digitalWrite(relaisLeft,LOW);
    //TODO : write the correct pin for the ESC + setup I2C connection 

    //TODO : write the correct pin for the ESC + setup I2C connection 
}

void loop(){
  	delay(500);
    if(receiveFlag){
        Serial.println("Received data");
        //TODO : write the correct pin for the ESC + setup I2C connection 
        Serial.println(temp);
        receiveFlag = false;
    }
}
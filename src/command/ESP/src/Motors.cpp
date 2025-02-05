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
#define relaisRight 1
#define relaisLeft 2

// Servo object to control the ESC
Servo esc;
Servo esc2;

// I2C received flag 
volatile boolean receiveFlag = false; // Drapeau pour la réception de données I2C


// I2C received data
char temp[32]; 


// joystick position : 
float x_sign;
float y_sign;


void convert_sign(float x, float y){
 // convert the y value : 
  // -1 1 
  // -127 128
  // 0 255 
  y_sign = (float)y*127/128;
  Serial.print("Sign y : ");
  Serial.println(y_sign);
  
  x_sign = (float)x*127/128;
  Serial.print("Sign x : ");
  Serial.println(x_sign);
  convert_unsign(x_sign,y_sign);
}

void convert_unsign(float x, float y){
  y_sign = (float)sqrt(y*y)*255;// absolute value to have 0 255 positive
  Serial.print("Unsign y : ");
  Serial.println(y_sign);
  x_sign = sqrt(x*x)*255; // absolute value to have 0 255 positive
  Serial.print("Unsign x : ");
  Serial.println(x_sign);
  
}


//Function for reading the received data
void onReceive(int len){
    for(int j=0; j<len; j++){
        temp[j] = Wire.read();
    }
    char* separator = strchr(temp,',');
    if(separator!=0){
        float a = atof(temp);
      	float b = atof(separator+1);
      	convert_sign(a,b);

      	analogWrite(5,x_sign);
      	analogWrite(6,y_sign);
        updateDirection();
    }    receiveFlag = true;
}



void updateDirection(){
  // we only consider y for the  direction 
  if(y_sign<0){
    digitalWrite(relaisRight,HIGH);
    digitalWrite(relaisLeft,HIGH);
  }
  else{
    digitalWrite(relaisRight,LOW);
    digitalWrite(relaisLeft,LOW);
  }
    
}

void setup(){
    Wire.onReceive(onReceive);
    Wire.begin((uint8_t)I2C_DEV_ADDR);
    Serial.begin(9600);
  	// setup the servo pinmode
  	pinMode(6,OUTPUT);
  	pinMode(5,OUTPUT);
  
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
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



// class for the motors : 
class Motor {
  private: 
  // the ESC objects
  Servo esc;
  Servo esc2;

  // the value of the joystick
  float xSign;
  float ySign;

  // the relay pins 
  int relaisRight;
  int relaisLeft;

  // the speed of the motors
  float rightSpeed;
  float leftSpeed;

  // Constructor : 
  Motor (int relaisRight, int relaisLeft, Servo esc, Servo esc2) {
    this->relaisRight = relaisRight;
    this->relaisLeft = relaisLeft;
    this->esc = esc;
    this->esc2 = esc2;
  }
  public:
  // Update the direction of the servo motors :
  void updateDirection(){
    // we only consider y for the  direction 
    if(ySign<0){
      digitalWrite(relaisRight,HIGH);
      digitalWrite(relaisLeft,HIGH);
    }
    else{
      digitalWrite(relaisRight,LOW);
      digitalWrite(relaisLeft,LOW);
    }
  }
  // function to convert receive float to sign 8 bytes float 
  void convert_unsign(float x, float y){
    ySign = (float)sqrt(y*y)*255;// absolute value to have 0 255 positive
    Serial.print("Unsign y : ");
    Serial.println(ySign);
    xSign = sqrt(x*x)*255; // absolute value to have 0 255 positive
    Serial.print("Unsign x : ");
    Serial.println(xSign);
  }

  // function to convert the received float to unsigned 8 bytes float
  void convert_sign(float x, float y){
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

  void stringToFloat(int len){
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
};

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
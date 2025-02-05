/*
  TRAVELERS version DELTA 
  ROLIN@2024
  
  Basé sur le code de controle COSTE@2024 et réception I2C TOURON@2022

  Ce programme contrôle un microcontrôleur ESP32 qui interfère avec deux ESCs 
  (Electronic Speed Controllers) et des moteurs via la communication I2C.
*/

#include <Arduino.h>
#include <ESP32Servo.h>
#include <Wire.h>

// Adresse I2C de l'appareil
#define I2C_DEV_ADDR 0x11

// Valeurs de seuil et coefficient pour la vitesse
const int dead = 35;
const int coeff_vit = 7.5;

// Pins pour les contrôles des moteurs et ESC
const int ControlL = 18;
const int ControlR = 5;
const int ESC1 = 4;
const int ESC2 = 15;

// Structure pour stocker les valeurs des moteurs
struct MotorValues {
  int leftValue;
  String leftDirection;
  int rightValue;
  String rightDirection;
};

// Objets Servo pour contrôler les ESC
Servo esc;
Servo esc2;
int throttle = 2000; // Valeur initiale de la manette des gaz

volatile boolean receiveFlag = false; // Drapeau pour la réception de données I2C
char temp[32]; // Buffer pour stocker les données reçues
int pwm;
String wheel, dir;

bool carre = false;

// Fonction appelée lors d'une demande I2C
void onRequest() {}

// Fonction appelée lors de la réception de données I2C
void onReceive(int len) {
  for (int j = 0; j < len; j++) {
    temp[j] = Wire.read();
    temp[j + 1] = '\0';
  }
  for (int j = 0; j < len; j++) {
    temp[j] = temp[j + 1];
  }
  Serial.println("interruption");
  receiveFlag = true;
}

// Fonction pour extraire les valeurs des moteurs à partir d'une chaîne de caractères
MotorValues MoveValues(String input_str) {
  MotorValues motorValues;
  input_str.remove(0, 2); // Retirer "M," du début de la chaîne
  char* msg = &input_str[0u];
  char* parts[5];
  int i = 0;
  parts[i] = strtok(msg, ",");
  while(parts[i] != NULL) {
    parts[++i] = strtok(NULL, ",");
  }
  motorValues.leftValue = atoi(parts[0]);
  motorValues.leftDirection = String(parts[1]);
  motorValues.rightValue = atoi(parts[2]);
  motorValues.rightDirection = String(parts[3]);
  return motorValues;
}

// Fonction pour déplacer les moteurs en fonction des valeurs et directions fournies
void Move(MotorValues motorValues) {
  int gauche = motorValues.leftValue;
  int droite = motorValues.rightValue;
  bool L_A = motorValues.leftDirection == "A";
  bool R_A = motorValues.rightDirection == "A";
  int valueR = 0;
  int valueL = 0;
  int speedR = 0;
  int speedL = 0;

  // Vérifier si les valeurs des moteurs dépassent le seuil
  if ((gauche <= -dead || gauche >= dead) || (droite <= -dead || droite >= dead)) {
    if ((droite <= -dead || droite >= dead)) {
      valueR = min((int)map(abs(droite), 0, 135, 0, 255), 255);
      speedR = abs(valueR) * coeff_vit;
    }
    if (gauche <= -dead || gauche >= dead) {
      valueL = min((int)map(abs(gauche), 0, 135, 0, 255), 255);
      speedL = abs(valueL) * coeff_vit;
    }

    // Limiter les vitesses à 2000 si dépassement éventuel
    if (speedR > 2000) {
      speedR = 2000;
    }
    if (speedL > 2000) {
      speedL = 2000;
    }

    // Déterminer la direction et régler les ESC en conséquence
    if (L_A) {
      digitalWrite(ControlL, HIGH);
      esc.writeMicroseconds(speedL);
    } else {
      digitalWrite(ControlL, LOW);
      esc.writeMicroseconds(speedL);
    }

    if (R_A) {
      digitalWrite(ControlR, HIGH);
      esc2.writeMicroseconds(speedR);
    } else {
      digitalWrite(ControlR, LOW);
      esc2.writeMicroseconds(speedR);
    }
  } else {
    // Si les valeurs sont en dessous du seuil, arrêter les moteurs
    digitalWrite(ControlL, HIGH);
    digitalWrite(ControlR, HIGH);
    esc.writeMicroseconds(1000);
    esc2.writeMicroseconds(1000);
  }
}

void setup() {
  // Initialisation de l'I2C et des interruptions
  Wire.onReceive(onReceive);
  Wire.onRequest(onRequest);
  Wire.begin((uint8_t)I2C_DEV_ADDR);

  Serial.begin(115200);

  // Attacher les objets Servo aux pins
  esc.attach(ESC1);
  esc2.attach(ESC2);
  
  delay(5000);

  // Configurer les pins de contrôle des moteurs comme sorties
  pinMode(ControlL, OUTPUT);
  pinMode(ControlR, OUTPUT);

  // Configurer la pin 2 comme sortie et la mettre à LOW
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);
}

void loop() {
  delay(10);
  if (receiveFlag) {
    String mess = String(temp);
    if (mess.charAt(0) == 'M') {
      MotorValues motorValues = MoveValues(mess);
      if (motorValues.leftDirection == "A") { // Moteur gauche en avant
        Serial.println("LA");
        Move(motorValues);
      } else if (motorValues.leftDirection == "R") { // Moteur gauche en arrière
        Serial.println("LR");
        Move(motorValues);
      }
      if (motorValues.rightDirection == "A") { // Moteur droit en avant
        Serial.println("RA");
        Move(motorValues);
      } else if (motorValues.rightDirection == "R") { // Moteur droit en arrière
        Serial.println("RR");
        Move(motorValues);
      }
    }
  }
  receiveFlag = false;
}
 
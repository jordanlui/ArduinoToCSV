/*  Script reads data from two Omron devices and analog sensors and outputs to serial.
 *  This script reads the data from a 8x1 OMRON D6T-8L sensor using only the Wire library. 
 *  Note that use of D6T-44L 4x4 sensor requires the WireExt.h library, so that the 35 bytes of data can be read from the sensor.
 *  Original code from Arduino forum on WireExt.h https://forum.arduino.cc/index.php?topic=217394.0
 
 *  
 *  Pin Assignments
 *  c0 Potentiometer on mux
 *  c1 Omron 8x1 on mux
 *  c2 omron 4x4 on mux
 *  A0, A1, A2 FSRs
 *  
 *  Other Info
 *  Multiplexer tutorial - http://bildr.org/2011/02/cd74hc4067-arduino/
 *  Multiplex the SDA signals and receive them on pin 0.
 *  All i2c component SCL lines connect to regular Arduino SCL line. 
 *  Note Arduino Uno i2c pin arrangements. A4 (SDA), A5 (SCL)
 *  Adding in the FSRs.
 *  
 *  
 */

#include <Wire.h>
#include <WireExt.h>
#include <elapsedMillis.h>
//elapsedMillis timeElapsed; // Global variable declaration for the elapsed time in the script as variable timeElapsed. Time output is not working yet :(


#define D6T_addr 0x0A // 7 bit address of OMRON D6T is 0x0A in hex
#define D6T_cmd 0x4C // Standard command is 4C in hex

int numbytes = 19; 
int numel = 8;
int rbuf[19]; // Actual raw data is coming in as 35 bytes for OMRON 4x4, and 19 bytes for Omron 8x1. 
int tdata[8]; // The data comming from the sensor is in 8 elements 
int rbuf2[35]; // Actual raw data is coming in as 35 bytes for OMRON 4x4, 
int tdata2[16]; // The data comming from the sensor is in 16 elements
float t_PTAT;

// Multiplexer setup
//Mux control pins
int s0 = 8;
int s1 = 9;
int s2 = 10;
int s3 = 11;
//Mux in "SIG" pin. The pin we actually receive and send signal to 
int SIG_pin = 0;

// Pin setups
int fsr1 = 0;
int fsr2 = 1;
int fsr3 = 2;

void setup()
{
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);

  digitalWrite(s0,LOW);
  digitalWrite(s1,LOW);
  digitalWrite(s2,LOW);
  digitalWrite(s3,LOW);
  
  
  Wire.begin();
  Serial.begin(9600);

}
 
void loop()
{

  
  // Display time elapsed
  Serial.print("Time,");
//  Serial.print(timeElapsed);
  Serial.print("\n");
  
  // Read from the potentiometer
  readMux(0);
//  int val
  int val = analogRead(A4);
  
  Serial.print("Potentiometer value is ");
  Serial.print(val);
  Serial.print("\n");
//  delay(20);
  
  // Reading from Omron 8x1
  // Omron 8x1 currently on address c1 on MUX.
  readMux(1);
  // SDA pin on Arduino should now be routed through MUX to the SDA on OMRON.
  int i;
  // Step one - send commands to the sensor
  delay(20);
  Wire.beginTransmission(D6T_addr);
  Wire.write(D6T_cmd);
  Wire.endTransmission();

  delay(50); // Delay between instruction and data acquisition

  // Read from the sensor
  // Need to send a read command here - but how will this work with 7 bit addressing?
  Wire.requestFrom(D6T_addr,numbytes); // D6T-8 returns 19 bytes 

  // Receive the data

  if (0 <= Wire.available()) { // If there is data still left in buffer, we acquire it.
    i = 0;
    for (i=0; i < numbytes; i++) {
      rbuf[i] = Wire.read();
    }
    t_PTAT = (rbuf[0] + (rbuf[1] << 8) ) * 0.1;
    Serial.print("Omron 8x8,");
    for (i = 0; i < numel; i++) {
      tdata[i] = (rbuf[(i*2+2)] + (rbuf[(i*2+3)] << 8 )) * 0.1;
      Serial.print(tdata[i]);
      Serial.print(",");
    }
    Serial.print("\n");
  }

  // Read from Omron 4x4
  readMux(2);
  // SDA pin on Arduino should now route to SDA for OMRON 4x4
  delay(20);
  Wire.beginTransmission(D6T_addr);
  Wire.write(D6T_cmd);
  Wire.endTransmission();
  delay(50);

  if (WireExt.beginReception(D6T_addr) >= 0) {
    i = 0;
    
    // Receive all our bytes of data
    for (i = 0; i < 35; i++) {
      rbuf[i] = WireExt.get_byte();
    }
    WireExt.endReception(); // End reception
    
    // Label our data as Omron 4x4
    Serial.print("OMRON 4x4,");
    
    t_PTAT = (rbuf[0]+(rbuf[1]<<8))*0.1; 
    // Calculate the individual element values
    for (i = 0; i < 16; i++) {
      tdata[i]=(rbuf[(i*2+2)]+(rbuf[(i*2+3)]<<8))*0.1;
      Serial.print(tdata[i]);
      Serial.print(",");
    } 
  }
  Serial.print("\n");

  // Read FSRs
  Serial.print("FSR1,");
  Serial.print(analogRead(fsr1));
  Serial.print("\n");

  Serial.print("FSR2,");
  Serial.print(analogRead(fsr2));
  Serial.print("\n");

  Serial.print("FSR3,");
  Serial.print(analogRead(fsr3));
  Serial.print("\n");
  

  
  

  Serial.print("\n");
  delay(500);          
}

int readMux(int channel){
  // Changes the addressing of the MUX.
  int controlPin[] = {s0, s1, s2, s3};

  int muxChannel[16][4]={
    {0,0,0,0}, //channel 0
    {1,0,0,0}, //channel 1
    {0,1,0,0}, //channel 2
    {1,1,0,0}, //channel 3
    {0,0,1,0}, //channel 4
    {1,0,1,0}, //channel 5
    {0,1,1,0}, //channel 6
    {1,1,1,0}, //channel 7
    {0,0,0,1}, //channel 8
    {1,0,0,1}, //channel 9
    {0,1,0,1}, //channel 10
    {1,1,0,1}, //channel 11
    {0,0,1,1}, //channel 12
    {1,0,1,1}, //channel 13
    {0,1,1,1}, //channel 14
    {1,1,1,1}  //channel 15
  };

  //loop through the 4 sig
  for(int i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }

  //read the value at the SIG pin
//  int val = analogRead(SIG_pin);

  //return the value
//  return val;
}
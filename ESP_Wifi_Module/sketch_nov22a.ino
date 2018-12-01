#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include "SparkFunLSM6DS3.h"
#include "Wire.h"
#include <SPI.h>
#include <RF24.h>
#include "MAX30105.h"

#include "heartRate.h"

MAX30105 particleSensor;

const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred

float beatsPerMinute;
int beatAvg;
LSM6DS3 myIMU; //Default constructor is I2C, addr 0x6B
int stepCounter = 0;
float posFinal = 1.5;
float negFinal = -1.5;
/* Set these to your desired credentials. */
const char *ssid = "UCInet Mobile Access";  //ENTER YOUR WIFI SETTINGS
const char *password = "dfghjk";
 
//Web/Server address to read/write from 
const char *host = "169.234.49.205";   //https://circuits4you.com website or IP address of server
 
//=======================================================================
//                    Power on setup
//=======================================================================
 
void setup() {
  delay(1000);
  Serial.begin(9600);
  WiFi.mode(WIFI_OFF);        //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA);        //This line hides the viewing of ESP as wifi hotspot
  myIMU.begin();
  WiFi.begin("UCInet Mobile Access", "dfghjk");     //Connect to your WiFi router
  Serial.println("");
 
  Serial.print("Connectingg");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
 
  //If connection successful show IP address in serial monitor
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //IP address assigned to your ESP

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  Serial.println("Place your index finger on the sensor with steady pressure.");

  particleSensor.setup(); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED
}
 
//=======================================================================
//                    Main Program Loop
//=======================================================================
void loop() {
  float inVal = myIMU.readFloatAccelZ();
  long irValue = particleSensor.getIR();

  Serial.println("hkhk");
  float outval = 0.0;
  if (inVal > posFinal) {
    while (true) {
      outval = myIMU.readFloatAccelZ();
      if (outval < negFinal){
        Serial.println(inVal);
        stepCounter =  stepCounter + 1;
        Serial.println("Step counter at:");
        //Serial.print(stepCounter);
        HTTPClient http;    //Declare object of class HTTPClient
 
        String ADCData, station, getData, Link;

        //GET Data
        Link = "http://169.234.49.205:5000/step";
  
        http.begin(Link);     //Specify request destination
  
        int httpCode = http.GET();            //Send the request
        String payload = http.getString();    //Get the response payload
 
        //Serial.println(httpCode);   //Print HTTP return code
        //Serial.println(payload);    //Print request response payload
 
        http.end();  //Close connection
        Serial.println("before break");
        delay(500);
        break;
      }
    }
  }

  if (checkForBeat(irValue) == true && irValue > 50000)
  {
    Serial.println("Helllllooooooo");
    int startTime = millis();
      //We sensed a beat!
      long delta = millis() - lastBeat;
      lastBeat = millis();

      beatsPerMinute = 60 / (delta / 1000.0);

      if (beatsPerMinute < 255 && beatsPerMinute > 20)
      {
        rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
        rateSpot %= RATE_SIZE; //Wrap variable

      //Take average of readings
        beatAvg = 0;
        for (byte x = 0 ; x < RATE_SIZE ; x++)
          beatAvg += rates[x];
        beatAvg /= RATE_SIZE;
      }

      Serial.println("IR=");
      Serial.println(irValue);
      Serial.println(", BPM=");
      Serial.println(beatsPerMinute);
      Serial.println(", Avg BPM=");
      Serial.println(beatAvg);
  } 
}

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <FastLED.h>
#include "utils.h"

//Тип подключения
//CONNECT_TYPE1 - x по горизонтали, y по вертикали
//CONNECT_TYPE2 - y по горизонтали, x по вертикали
//INVERT_X - инвертировать по x
//INVERT_Y - инвертировать по y
#define CONNECT_TYPE1 
//#define CONNECT_TYPE2
#define INVERT_X
#define INVERT_Y

#define CORRECTION 0xFFEFF0
#define LED_ORDER GRB
#define LED_TYPE WS2812

#define MAX_BRIGHTNESS 100

#define NUM_LEDS_X 5
#define NUM_LEDS_Y 5
#define MATRIX_PIN 15

#define WIFI_SSID ""
#define WIFI_PASS ""

#define NUM_LEDS (NUM_LEDS_X*NUM_LEDS_Y)

#define UPDATE_MODE_DELAY 60
#define MAX_FPS 60

#define INFO_NAME "Mrybs` Public Matrix"
#define INFO_ABOUT "---"
#define INFO_PROGRAM_NAME "Mrybs` Public Matrix Firmware"
#define INFO_MAJOR_VERSION "1"
#define INFO_MINOR_VERSION "0"
#define INFO_BUILD "260623A"
#define INFO_BUILD_TYPE "SNAPSHOT"
#define INFO_BUILD_SUBTYPE "REFACTOR"
#define INFO_DEBUG "SERIAL_INDICATOR"


CRGB leds[NUM_LEDS];
ESP8266WebServer server(80);

long long FPSControl = 0;
long long DrawingControl = 0;
int seed_x = 0;
int seed_y = 0;
int frame = 0;
byte breathBrightness = 50;
bool breathBrightnessDirection = true;
String effect_id = "ball";
bool showingEffect = true;
String mode_id = "none";

int sins_x[NUM_LEDS_X];
int sins_y[NUM_LEDS_Y];

byte sChance = 20;
byte sHue = 127;
byte sSaturation = 0;
int sSpeed = 256;


void setup() {
  pinMode(13, OUTPUT);
  countXSin();
  countYSin();
  FastLED.addLeds<LED_TYPE, MATRIX_PIN, LED_ORDER>(leds, NUM_LEDS).setCorrection(CORRECTION);

  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.println("");
  for(int i = 0; i < NUM_LEDS; i++){
    leds[i] = CRGB(0, 50, 50);
    FastLED.show();
  }
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    Serial.print(".");
  }
  Serial.println("\nConnected");
  Serial.println(WiFi.localIP());
  ArduinoOTAInit();
  for(int i = 0; i < NUM_LEDS; i++){
    leds[i] = CRGB(60, 50, 0);
  }
  FastLED.show();

  server.on("/api", HTTP_GET, handleApi);
  server.begin();
}


void loop() {
  server.handleClient();
  ArduinoOTA.handle();
  showEffect();
  showMode();
  frame++;
  if(frame == MAX_FPS) frame = 0;
  seed_y++;
  if(seed_y == NUM_LEDS_Y) seed_y = 0;
  seed_x++;
  if(seed_x == NUM_LEDS_X) seed_x = 0;
  if(millis() - FPSControl > 1000/MAX_FPS){
    FPSControl = millis();
    FastLED.show();
  }
}

void ArduinoOTAInit(){
  ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH) {type = "sketch";} else {type = "filesystem";}
    Serial.println("Start updating " + type);
  });
  ArduinoOTA.onEnd([]() {Serial.println("\nEnd");});
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {Serial.printf("Progress: %u%%\r", (progress / (total / 100)));});
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) {
      Serial.println("Auth Failed");
    } else if (error == OTA_BEGIN_ERROR) {
      Serial.println("Begin Failed");
    } else if (error == OTA_CONNECT_ERROR) {
      Serial.println("Connect Failed");
    } else if (error == OTA_RECEIVE_ERROR) {
      Serial.println("Receive Failed");
    } else if (error == OTA_END_ERROR) {
      Serial.println("End Failed");
    }
  });
  ArduinoOTA.begin();
  Serial.println("OTA Ready");
}

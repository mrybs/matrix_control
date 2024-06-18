#include <ESP8266WiFi.h>
//#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ESPAsyncWebServer.h>
#include <FS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <FastLED.h>
//#include <ESPAsyncTCP.h>
#include <WiFiClient.h>
#include "Vector.h"
#include "arg.h"
#include "utils.h"
#include "response.h"

//Тип подключения
//CONNECT_TYPE1 - x по горизонтали, y по вертикали
//CONNECT_TYPE2 - y по горизонтали, x по вертикали
//
//INVERT_X - инвертировать по x
//INVERT_Y - инвертировать по y
#define CONNECT_TYPE1 
//#define CONNECT_TYPE2
//#define INVERT_X
//#define INVERT_Y

#define CORRECTION 0xDFDD64
#define LED_ORDER GRB
#define LED_TYPE WS2812

#define MAX_BRIGHTNESS 100

#define NUM_LEDS_X 16
#define NUM_LEDS_Y 16
#define MATRIX_PIN 15

#define WIFI_SSID "Mekakay"
#define WIFI_PASS "123zxc456vbn"
//#define WIFI_CHANNEL 1
//#define MMATRIX_TOKEN "mx.t.fa.mrybsmatrix:f0ca9b1ed21b01c515612f0bcc31ebcbdc899ed8d6c85a4f94eeb527f052fb8d_ca781836951a4c6f66dc26f946af717257c9bf5f4110259492746d530f03f83b" 
//#define MMATRIX_IP "192.168.50.122"
//#define MMATRIX_PPS 0.5

#define WAVES_AMOUNT 2
#define BALLS_AMOUNT 3

#define NUM_LEDS (NUM_LEDS_X*NUM_LEDS_Y)

#define UPDATE_MODE_DELAY 60
#define MAX_FPS 30 //около 30мкс на один пиксель + передача

#define INFO_NAME "Mrybs` Public Matrix"
#define INFO_ABOUT "Mrybs` Public Matrix standart firmware. https://github.com/mrybs/matrix_control/"
#define INFO_PROGRAM_NAME "Mrybs` Public Matrix firmware"
#define INFO_MAJOR_VERSION "1"
#define INFO_MINOR_VERSION "0"
#define INFO_BUILD "140624a"
#define INFO_BUILD_TYPE "SNAPSHOT"
#define INFO_BUILD_SUBTYPE "NEW"

#define EFFECTS {"balls", "rainbow", "color_explosion", "confetti", "sinusoid", "snowing", "perlin", "lava"}
//#define OTA_ENABLE

struct Vector2{
  float x;
  float y;
};

struct Ball{
  Vector2 position;
  Vector2 velocity;
};

CRGB leds[NUM_LEDS];
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

long long FPSControl = 0;
long long DrawingControl = 0;
#ifdef MMATRIX_TOKEN
  long long PollingControl = 0;
#endif
byte breathBrightness = 50;
bool breathBrightnessDirection = true;
String effect_id = "balls";
bool showingEffect = true;
String mode_id = "none";

byte sChance = 20;
byte sHue = 127;
byte sSaturation = 0;
int sSpeed = 256;
bool sRainbow = false;
float sScale = 1;

byte sBrightness = 100;

byte w[WAVES_AMOUNT];
byte phi[WAVES_AMOUNT];
byte A[WAVES_AMOUNT];
Ball balls[BALLS_AMOUNT];

void setup() {
  ESP.wdtEnable(0);
  FastLED.addLeds<LED_TYPE, MATRIX_PIN, LED_ORDER>(leds, NUM_LEDS).setCorrection(CORRECTION);

#ifdef WIFI_CHANNEL
  WiFi.begin(WIFI_SSID, WIFI_PASS, WIFI_CHANNEL);
#else
  WiFi.begin(WIFI_SSID, WIFI_PASS);
#endif
  Serial.begin(115200);
  Serial.println("\nLoading...");
  Serial.println("Checking matrix...");
  for(int i = 0; i < NUM_LEDS; i++){
    leds[i] = CRGB(0, 50, 50);
    FastLED.show();
  }
  Serial.println("Initialising effects...");

  for(short i = 0; i < BALLS_AMOUNT; i++){
    balls[i] = {
      {float(rand()%100)/100, float(rand()%100)/100},
      {float(rand()%100)/100, float(rand()%100)/100}
    };
  }
  Serial.println("Balls created");
  Serial.println("Initialising filesystem...");
  SPIFFSConfig cfg;
  cfg.setAutoFormat(false);
  SPIFFS.setConfig(cfg);
  SPIFFS.begin();
  Dir dir = SPIFFS.openDir("/");
  while(dir.next()){
    Serial.println(dir.fileName());
  }
  Serial.print("Trying to connect to ");
  Serial.print(WIFI_SSID);
  Serial.println("(1 min)");
  Serial.print("Connecting");
  short tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 60) {
    delay(1000);
    Serial.print(".");
    tries++;
  }
  if(WiFi.status() == WL_CONNECTED){
    Serial.println("\nConnected ("+String(tries)+" tries)");
    Serial.print("You can open the control panel at http://");
    Serial.print(WiFi.localIP());
    Serial.println("/");
  }
  else Serial.println("\nDid not connect");
#ifdef OTA_ENABLE
  ArduinoOTAInit();
#endif
  for(int i = 0; i < NUM_LEDS; i++){
    leds[i] = CRGB(60, 50, 0);
  }
  FastLED.show();

  server.on("/api", HTTP_GET, handleGETApi);
  server.on("/api", HTTP_POST, [](AsyncWebServerRequest *request) {}, NULL, handlePOST);
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    File f = SPIFFS.open("/index.html", "r");
    if(!f) return request->send(500, "plain/text", "Could not open file index.html");
    request->send(200, "text/html", f.readString().c_str());
    f.close();
  });
  server.on("/index.js", HTTP_GET, [](AsyncWebServerRequest *request){
    File f = SPIFFS.open("/index.js", "r");
    if(!f) return request->send(500, "plain/text", "Could not open file index.js");
    request->send(200, "text/javascript", f.readString().c_str());
    f.close();
  });
  server.on("/styles.css", HTTP_GET, [](AsyncWebServerRequest *request){
    File f = SPIFFS.open("/styles.css", "r");
    if(!f) return request->send(500, "plain/text", "Could not open file styles.css");
    request->send(200, "text/css", f.readString().c_str());
    f.close();
  });
  server.on("/canvas.js", HTTP_GET, [](AsyncWebServerRequest *request){
    File f = SPIFFS.open("/canvas.js", "r");
    if(!f) request->send(500, "plain/text", "Could not open file canvas.js");
    request->send(200, "text/javascript", f.readString().c_str());
    f.close();
  });
  ws.onEvent(onEvent);
  server.addHandler(&ws);
  server.begin();

  #ifdef MMATRIX_TOKEN
    AsyncClient *client = new AsyncClient;
    String hostname = MMATRIX_IP;
    const int port = 8000;
    const String url = "/api/poll?matrix_token="+String(MMATRIX_TOKEN);
    String http = "GET " + url + " HTTP/1.1\r\nHost: " + hostname + ":" + String(port) + "\r\n\r\n";
    Serial.println(http);
    client->onConnect([&](void *arg, AsyncClient* c){
      Serial.printf("\n client has been connected to %s on port %d \n", hostname.c_str(), port);
      reinterpret_cast<AsyncClient*>(c)->write(http.c_str());
    }, client);
    client->onData([&](void *arg, AsyncClient *c, void *data, size_t len){
      Serial.printf("\n data received from %s \n", c->remoteIP().toString().c_str());
      Serial.write((uint8_t*)data, len);
    }, client);

    client->connect(hostname.c_str(), port);
  #endif
} 

void onEvent(AsyncWebSocket * server, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t *data, size_t len) {
  if(type == WS_EVT_DATA) {
    if(strcmp((const char*)data, "get_matrix") == 0){
      char* image = new char[NUM_LEDS*3];
      for(int i = 0; i < NUM_LEDS; i++){
        #ifdef INVERT_X
          short x = NUM_LEDS_X - i%NUM_LEDS_X - 1;
        #else
          short x = i%NUM_LEDS_X;
        #endif
        #ifdef INVERT_Y
          short y = NUM_LEDS_Y - i/NUM_LEDS_Y - 1;
        #else
          short y = i/NUM_LEDS_Y;
        #endif
        #ifdef CONNECT_TYPE1
          if(y%2==1) x=abs(x-NUM_LEDS_X+1);
          memcpy(image+i*3, (const char*)leds[NUM_LEDS_Y*y+x].raw, 3);
        #elif CONNECT_TYPE2
          if(x%2==1) y=abs(y-NUM_LEDS_Y+1);
          memcpy(image+i*3, (const char*)leds[NUM_LEDS_X*x+y].raw, 3);
        #endif
      }
      client->binary(image, NUM_LEDS*3);
      delete image;
    }
  } else if(type == WS_EVT_CONNECT) {
    Serial.printf("Client connected: %u\n", client->id());
  } else if(type == WS_EVT_DISCONNECT) {
    Serial.printf("Client disconnected: %u\n", client->id());
  }
}


void loop() {
  //server.handleClient();
#ifdef OTA_ENABLE
  ArduinoOTA.handle();
#endif
  
#ifdef MMATRIX_TOKEN
  if(millis() - PollingControl > 1000/MMATRIX_PPS){
    PollingControl = millis();
    serverPoll();
  }
#endif
  showEffect();
  FastLED.show();
}

Vector<String> strsplit(String str, char d){
  Vector<String> result;
  String line = "";
  for(int i = 0; i < str.length(); i++){
    if(str[i] == d){
      result.Append(line);
      line = "";
    }else
      line += str[i];
  }
  result.Append(line);
  return result;
}

Vector<arg> strToArgs(String args){
  Vector<arg> result;
  Vector<String> params = strsplit(args, '&');
  for(int i = 0; i < params.getLength(); i++){
    String param = params.getByIndex(i);
    Vector<String> KD = strsplit(param, '=');
    result.Append(arg(KD.getByIndex(0), KD.getByIndex(1)));
  }
  return result;
}

#ifdef MMATRIX_TOKEN
void serverPoll(){
  /*
  AsyncClient *client = new AsyncClient;
  const String hostname = String(MMATRIX_IP);
  const int port = 8000;
  const String url = "/api/poll?matrix_token="+String(MMATRIX_TOKEN);
  Serial.println("GET " + url + " HTTP/1.1\r\nHost: " + hostname + ":" + String(port) + "\r\n\r\n");
  client->onConnect([&](void *arg, AsyncClient* client){
    Serial.printf("\n client has been connected to %s on port %d \n", hostname, port);
    reinterpret_cast<AsyncClient*>(client)->write(String("GET " + url + " HTTP/1.1\r\nHost: " + hostname + ":" + String(port) + "\r\n\r\n").c_str());
  }, client);
  client->onData([&](void *arg, AsyncClient *c, void *data, size_t len){
    Serial.printf("\n data received from %s \n", client->remoteIP().toString().c_str());
    Serial.write((uint8_t*)data, len);
  }, client);

  
  Serial.println("GET " + url + " HTTP/1.1\r\nHost: " + hostname + ":" + String(port) + "\r\n\r\n");
  client->connect(hostname.c_str(), port);

  */
  //http.init("GET", "http://"+String(MMATRIX_IP)+"/api/poll?matrix_token="+String(MMATRIX_TOKEN));
  /*int HTTPCode = http.GET();
  if(HTTPCode != 200) return;
  String polls = http.getString();
  http.end();
  String line = "";
  if(polls != "") Serial.println(polls);
  for(int i = 0; i < polls.length(); i++){
    if(polls[i] == '\n'){
      handle("/api", strToArgs(line));
    }else{
      line += polls[i];
    }
  }*/
}
#endif
#ifdef OTA_ENABLE
void ArduinoOTAInit(){
  ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH) type = "sketch"; else type = "filesystem";
    Serial.println("Start updating " + type);
  });
  ArduinoOTA.onEnd([]() {Serial.println("\nEnd");});
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {Serial.printf("Progress: %u%%\r", (progress / (total / 100)));});
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR)
      Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR)
      Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR)
      Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) 
      Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) 
      Serial.println("End Failed");
  });
  ArduinoOTA.begin();
  Serial.println("OTA Ready");
}
#endif

#include <Arduino.h>

struct response{
  int code = 200;
  String type = "text/plain";
  String data = "";
  response(int code, String type, String data){
    this->code = code;
    this->type = type;
    this->data = data;
  }
};
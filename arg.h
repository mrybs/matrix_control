#include <Arduino.h>

struct arg{
  String key;
  String data;
  arg(String key, String data){
    this->key = key;
    this->data = data;
  }
};
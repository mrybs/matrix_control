#include <Arduino.h>

struct Utils{
  static byte stoh(String str){
    char string[str.length()];
    str.toCharArray(string, str.length());
    return (byte) strtol(string, 0, 16);
  }
};
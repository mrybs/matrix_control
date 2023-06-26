#include "utils.h"

byte strToHex(String str){
  char string[str.length()];
  str.toCharArray(string, str.length());
  return (byte) strtol(string, 0, 16);
}
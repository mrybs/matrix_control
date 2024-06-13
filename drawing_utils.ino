void drawPixel(int x, int y, CRGB color){
  #ifdef INVERT_X
    x = NUM_LEDS_X - x - 1;
  #endif
  #ifdef INVERT_Y
    y = NUM_LEDS_Y - y - 1;
  #endif
  #ifdef CONNECT_TYPE1
    if(y%2==1) x=abs(x-NUM_LEDS_X+1);
    leds[NUM_LEDS_Y*y+x] = color;
  #elif CONNECT_TYPE2
    if(x%2==1) y=abs(y-NUM_LEDS_Y+1);
    leds[NUM_LEDS_X*x+y] = color;
  #endif
}

void drawPixelByIndex(int index, CRGB color){
  drawPixel(index%NUM_LEDS_X, index/NUM_LEDS_Y, color);
}

CRGB getPixel(int x, int y){
  #ifdef INVERT_X
    x = NUM_LEDS_X - x - 1;
  #endif
  #ifdef INVERT_Y
    y = NUM_LEDS_Y - y - 1;
  #endif
  #ifdef CONNECT_TYPE1
    if(y%2==1) x=abs(x-NUM_LEDS_X+1);
    return leds[NUM_LEDS_Y*y+x];
  #elif CONNECT_TYPE2
    if(x%2==1) y=abs(y-NUM_LEDS_Y+1);
    return leds[NUM_LEDS_X*x+y];
  #endif
}

CRGB getPixelByIndex(int index){
  return getPixel(index%NUM_LEDS_X, index/NUM_LEDS_Y);
}

void moveX(){
  CRGB buffer[NUM_LEDS_Y][NUM_LEDS_X];
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      buffer[y][x] = getPixel(x, y);

  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 1; x < NUM_LEDS_X; x++)
      buffer[y][x] = getPixel(x-1, y);

  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      drawPixel(x, y, buffer[y][x]);
}

void moveY(){
  CRGB buffer[NUM_LEDS_Y][NUM_LEDS_X];
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      buffer[y][x] = getPixel(x, y);

  for(int y = 1; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      buffer[y][x] = getPixel(x, y-1);

  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      drawPixel(x, y, buffer[y][x]);
}


void fill(CRGB color){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      drawPixel(x, y, color);
}

byte calcNoise(int x, int y){
  return ABS(pnoise(double(x)/NUM_LEDS_X/sScale/1.25+double(millis())/511, double(y)/NUM_LEDS_Y/sScale/1.25+double(millis())/511, double((sSpeed/511)*abs(1000-(DrawingControl%1000-250))%1000)/1500)*511+millis()/2);
}

byte getBrightness(){
  return round(double(sBrightness)*double(MAX_BRIGHTNESS)*0.0255);
}
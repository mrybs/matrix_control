float ballPositionX=0.0f;
float ballPositionY=0.0f;
float ballVelocityX=0.67f;
float ballVelocityY=0.33f;

void eSinusoid(){
  moveX();
  int sinus = getYSin();
  Serial.println(sinus);
  for(int y = 0; y < NUM_LEDS_Y; y++)
    if(sinus==y)
      drawPixel(0, y, CHSV(sHue, sSaturation, 255));
    else
      drawPixel(0, y, CRGB(0,0,0));
}

void eSnowing(){
  moveY();
  for(int x = 0; x < NUM_LEDS_X; x++){
    if(rand()%100<sChance)
      drawPixel(x, 0, CHSV(sHue+millis(), sSaturation, 255));
    else
      drawPixel(x, 0, CRGB(0,0,0));
  }
}

void eDoubleWave(){
  moveX();
  moveY();
  int sinus = getYSin();
  for(int y = 0; y < NUM_LEDS_Y; y++)
    if(sinus==y)
      drawPixel(0, y, CHSV(sHue, sSaturation, 255));
    else
      drawPixel(0, y, CRGB(0,0,0));
  sinus = getXSin();
  for(int x = 0; x < NUM_LEDS_X; x++)
    if(sinus==x)
      drawPixel(x, 0, CHSV(sHue, sSaturation, 255));
    else
      drawPixel(x, 0, CRGB(0,0,0));
}

void eRainbow(){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      drawPixel(x, y, CHSV((y+1)*255/NUM_LEDS_Y+(x+1)*255/NUM_LEDS_X+millis(), 255, 255));
}


void eBall(){
  fill(CRGB(0,0,0));
  drawPixel(ballPositionX, ballPositionY, CHSV(millis(), 255, 255));
  ballPositionX+=ballVelocityX;
  ballPositionY+=ballVelocityY;
  if(ballPositionX < 0 || ballPositionX > NUM_LEDS_X-1) {
    ballVelocityX = -ballVelocityX;
  }
  if(ballPositionY < 0 || ballPositionY > NUM_LEDS_Y-1) {
    ballVelocityY = -ballVelocityY;
  }
}
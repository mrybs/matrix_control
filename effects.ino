float ballPositionX=0.0f;
float ballPositionY=0.0f;
float ballVelocityX=0.55f;
float ballVelocityY=0.45f;

void eRainbow(){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      drawPixel(x, y, CHSV((y+1)*255/NUM_LEDS_Y+(x+1)*255/NUM_LEDS_X+millis()*sSpeed/250, 255, 255));
}

void eConfetti(){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      drawPixel(x, y, CHSV((y+1)*255/NUM_LEDS_Y+(x+1)*255/NUM_LEDS_X+rand(), 255, 255));
}

int t = 0;
void eSinusoid(){
  moveX();
  for(int y = 0; y < NUM_LEDS_Y; y++)
    drawPixel(0, y, CRGB::Black);
  t++;
  if (t > 360) t = 0;
  float value = NUM_LEDS_X / 2 + (float)A[0] * sin((float)w[0] * t * 0.017453 + (float)phi[0] * DEG_TO_RAD);
  drawPixel(0, value, CHSV(sHue+millis()*int(sRainbow), sSaturation, 255));
}

void eSnowing(){
  moveY();
  for(int x = 0; x < NUM_LEDS_X; x++){
    if(rand()%100<sChance)
      drawPixel(x, 0, CHSV(sHue+millis()*int(sRainbow), sSaturation, 255));
    else
      drawPixel(x, 0, CRGB(0,0,0));
  }
}

void eBall(){
  fill(CRGB(0,0,0));
  drawPixel(ballPositionX, ballPositionY, CHSV(sHue+millis()*int(sRainbow), 255, 255));
  ballPositionX+=ballVelocityX;
  ballPositionY+=ballVelocityY;
  if(ballPositionX < 0 || ballPositionX > NUM_LEDS_X-1) ballVelocityX = -ballVelocityX;
  if(ballPositionY < 0 || ballPositionY > NUM_LEDS_Y-1) ballVelocityY = -ballVelocityY;
}

void eSquare(){
  
}

void ePerlin(){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++){
      byte noise = calcNoise(x, y);
      drawPixel(x, y, CHSV(noise, sSaturation, 255));
    }
}

void eLava(){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++){
      byte noise = calcNoise(x, y);
      drawPixel(x, y, CHSV(noise/5+sHue, 255, 255));
    }
}

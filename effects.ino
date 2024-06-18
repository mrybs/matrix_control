void eRainbow(){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      drawPixel(x, y, CHSV((y+1)*255/NUM_LEDS_Y+(x+1)*255/NUM_LEDS_X+millis()*sSpeed/250, 255, 255));
}

void eConfetti(){
  fill(CRGB(0,0,0), 0.20f);
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++)
      if(rand()%50==0)
        drawPixel(x, y, CHSV((y+1)*255/NUM_LEDS_Y+(x+1)*255/NUM_LEDS_X+rand(), sSaturation, 255));
}

void eColorExplosion(){
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
  drawPixel(0, value, CHSV(sHue+millis()/10*int(sRainbow), sSaturation, 255));
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
  fill(CRGB(0,0,0), 0.25f);
  for(short i = 0; i < BALLS_AMOUNT; i++){
    drawPixel(balls[i].position.x, balls[i].position.y, CHSV((255/BALLS_AMOUNT*i)+millis()*int(sRainbow)/10, sSaturation, 255));
    balls[i].position.x+=balls[i].velocity.x;
    balls[i].position.y+=balls[i].velocity.y;
    if(balls[i].position.x < 0 || balls[i].position.x > NUM_LEDS_X-1) balls[i].velocity.x = -balls[i].velocity.x;
    if(balls[i].position.y < 0 || balls[i].position.y > NUM_LEDS_Y-1) balls[i].velocity.y = -balls[i].velocity.y;
  }
}

void eBreathingSquare(){
  
}

void ePerlin(){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++){
      byte noise = calcNoise(x, y);
      drawPixel(x, y, CHSV(noise, sSaturation, 255-noise*(255-sSaturation)));
    }
}

void eLava(){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    for(int x = 0; x < NUM_LEDS_X; x++){
      byte noise = calcNoise(x, y);
      drawPixel(x, y, CHSV(noise/5+sHue+millis()*int(sRainbow)/10, 255, 255-noise/2));
    }
}

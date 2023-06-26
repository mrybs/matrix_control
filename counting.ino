int getXSin(){
  return sins_x[seed_x];
}

int getYSin(){
  return sins_y[seed_y];
}

void countXSin(){
  for(int x = 0; x < NUM_LEDS_X; x++)
    sins_x[x] = int((sin((x%NUM_LEDS_X)*6.28/NUM_LEDS_X)+1)/2*(NUM_LEDS_X-1)*1.1);
}

void countYSin(){
  for(int y = 0; y < NUM_LEDS_Y; y++)
    sins_y[y] = int((sin((y%NUM_LEDS_Y)*6.28/NUM_LEDS_Y)+1)/2*(NUM_LEDS_Y-1)*1.1);
}
void randomSinusoid(){
  for (byte j = 0; j < WAVES_AMOUNT; j++) {
      w[j] = random(17, 25);
      phi[j] = random(0, 360);
      A[j] = NUM_LEDS_X / 2 * random(4, 11) / 10;
  }
}

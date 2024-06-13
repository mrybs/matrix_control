void showEffect(){
  FastLED.setBrightness(getBrightness());
  if(effect_id == "rainbow"){
    eRainbow();
  }
  else if(effect_id == "confetti"){
    if(millis() - DrawingControl > 10000/sSpeed){
      DrawingControl = millis();
      eConfetti();
    }
  }
  else if(effect_id == "sinusoid"){
    if(millis() - DrawingControl > 10000/sSpeed){
      DrawingControl = millis();
      eSinusoid();
    }
  }
  else if(effect_id == "snowing"){
    if(millis() - DrawingControl > 10000/sSpeed){
      DrawingControl = millis();
      eSnowing();
    }
  }
  else if(effect_id == "ball"){
    if(millis() - DrawingControl > 10000/sSpeed){
      DrawingControl = millis();
      eBall();
    }
  }
  else if(effect_id == "perlin"){
    DrawingControl = millis();
    ePerlin();
  }
  else if(effect_id == "lava"){
    DrawingControl = millis();
    eLava();
  }
}

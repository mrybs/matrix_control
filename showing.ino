void showEffect(){
  if(effect_id == "rainbow"){
    DrawingControl = millis();
    eRainbow();
  }
  if(effect_id == "confetti"){
    if(millis() - DrawingControl > 10000/sSpeed){
      DrawingControl = millis();
      eConfetti();
    }
  }
  if(effect_id == "sinusoid"){
    if(millis() - DrawingControl > 10000/sSpeed){
      DrawingControl = millis();
      eSinusoid();
    }
  }
  if(effect_id == "snowing"){
    if(millis() - DrawingControl > 10000/sSpeed){
      DrawingControl = millis();
      eSnowing();
    }
  }
  if(effect_id == "doubleSinusoid"){
    if(millis() - DrawingControl > 10000/sSpeed){
      DrawingControl = millis();
      eDoubleWave();
    }
  }
  if(effect_id == "ball"){
    if(millis() - DrawingControl > 10000/sSpeed){
      DrawingControl = millis();
      eBall();
    }
  }
}

void showMode(){

}
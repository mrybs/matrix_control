void handleApi() {
  digitalWrite(13, 1);
  if(server.hasArg("function")){
    String function = server.arg("function");
    if(function == "fill"){
      byte r = 0;
      byte g = 0;
      byte b = 0;

      if (server.hasArg("r"))
        r = server.arg("r").toInt();
      if (server.hasArg("g"))
        g = server.arg("g").toInt();
      if (server.hasArg("b"))
        b = server.arg("b").toInt();

      for(int i = 0; i < NUM_LEDS; i++){
        leds[i] = CRGB(r, g, b);
      }
    }
    if(function == "pixel"){
      int x = 0;
      int y = 0;
      byte r = 0;
      byte g = 0;
      byte b = 0;
      
      if(server.hasArg("x")){
        String argX = server.arg("x");
        if (argX.toInt() < NUM_LEDS_X && -1 < argX.toInt()) x = argX.toInt();
      }
      if(server.hasArg("y")){
        String argY = server.arg("y");
        if (argY.toInt() < NUM_LEDS_Y && -1 < argY.toInt())
          y = argY.toInt();
      }
      if (server.hasArg("r")){
        String argR = server.arg("r");
        r = argR.toInt();
      }
      if (server.hasArg("g")){
        String argG = server.arg("g");
        g = argG.toInt();
      }
      if (server.hasArg("b")){
        String argB = server.arg("b");
        b = argB.toInt();
      }
      drawPixel(x, y, CRGB(r, g, b));
    }
    if(function == "image"){
      if(!server.hasArg("image")){
        server.send(200, "text/plain", "No image specified");
        digitalWrite(13, 0);
        return;
      }
      String image = server.arg("image");
      Serial.println(image);
      for(int i = 0; i < NUM_LEDS; i++){
        Serial.print(strToHex(String(image[i*8])+"0")*15 + strToHex(String(image[i*8+1])+"0"));
        Serial.print(", ");
        Serial.print(strToHex(String(image[i*8+2])+"0")*15 + strToHex(String(image[i*8+3]+"0")));
        Serial.print(", ");
        Serial.print(strToHex(String(image[i*8+4])+"0")*15 + strToHex(String(image[i*8+5]+"0")));
        Serial.println("");
        drawPixelByIndex(i, CRGB(
          strToHex(String(image[i*8])+"0")*15 + strToHex(String(image[i*8+1])+"0"),
          strToHex(String(image[i*8+2])+"0")*15 + strToHex(String(image[i*8+3])+"0"),
          strToHex(String(image[i*8+4])+"0")*15 + strToHex(String(image[i*8+5])+"0")
        ));
      }
    }
    if(function == "getInfo"){
      server.send(200, "text/plain", String("NAME:") + INFO_NAME + 
                                     String(";ABOUT:") + INFO_ABOUT + 
                                     String(";PROGRAM_NAME:") + INFO_PROGRAM_NAME + 
                                     String(";MAJOR_VERSION:") + INFO_MAJOR_VERSION + 
                                     String(";MINOR_VERSION:") + INFO_MINOR_VERSION + 
                                     String(";BUILD:") + INFO_BUILD +
                                     String(";TYPE:") + INFO_BUILD_TYPE +
                                     String(";SUBTYPE:") + INFO_BUILD_SUBTYPE +
                                     String(";DEBUG:") + INFO_DEBUG);
      digitalWrite(13, 0);
      return;
    }
    if(function == "effect"){
      if(!server.hasArg("effect")){
        server.send(200, "text/plain", "No effect specified");
        digitalWrite(13, 0);
        return;
      }
      effect_id = server.arg("effect");
    }
  }
  digitalWrite(13, 0);
  server.send(200, "text/plain", "OK");
}

void setBrightness(byte brightness){
  FastLED.setBrightness(MAX_BRIGHTNESS*brightness/39-2);
}
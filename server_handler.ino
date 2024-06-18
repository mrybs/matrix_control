AsyncWebServerResponse* ApiResponse(AsyncWebServerRequest *request, response R) {
  AsyncWebServerResponse *response;
  response = request->beginResponse(R.code, R.type, R.data);
  response->addHeader("Access-Control-Allow-Origin", "*");
  response->addHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  response->addHeader("Access-Control-Allow-Headers", "Content-Type,Authorization");
  return response;
}

void handleGETApi(AsyncWebServerRequest *request) {
  Vector<arg> args;
  for (uint8_t i = 0; i < request->args(); i++) {
    args.Append(arg(request->argName(i), request->arg(i)));
  }
  request->send(ApiResponse(request, handleGET("/api", args)));
}

void setBrightness(byte brightness){
  FastLED.setBrightness(MAX_BRIGHTNESS*brightness/39-2);
}

response handleGET(String path, Vector<arg> args){
  if(path == "/api"){
    if(findArg(args, "function")){
      String function = getArg(args, "function");
      if(function == "fill"){
        byte r = 0;
        byte g = 0;
        byte b = 0;

        if (findArg(args, "r")) r = getArg(args, "r").toInt();
        if (findArg(args, "g")) g = getArg(args, "g").toInt();
        if (findArg(args, "b")) b = getArg(args, "b").toInt();

        fill(CRGB(r, g, b));
        effect_id = "off";
        return response(200, "text/plain", "OK");
      }
      if(function == "pixel"){
        int x = 0;
        int y = 0;
        byte r = 0;
        byte g = 0;
        byte b = 0;
        
        if(findArg(args, "x")){
          String argX = getArg(args, "x");
          if (argX.toInt() < NUM_LEDS_X && -1 < argX.toInt()) x = argX.toInt();
        }
        if(findArg(args, "y")){
          String argY = getArg(args, "y");
          if (argY.toInt() < NUM_LEDS_Y && -1 < argY.toInt()) y = argY.toInt();
        }
        if (findArg(args, "r")){
          String argR = getArg(args, "r");
          r = argR.toInt();
        }
        if (findArg(args, "g")){
          String argG = getArg(args, "g");
          g = argG.toInt();
        }
        if (findArg(args, "b")){
          String argB = getArg(args, "b");
          b = argB.toInt();
        }
        drawPixel(x, y, CRGB(r, g, b));
        effect_id = "off";
        return response(200, "text/plain", "OK");
      }
      if(function == "getInfo"){
        String info = String("{\"name\": \"") + INFO_NAME + 
                      String("\", \"about\": \"") + INFO_ABOUT + 
                      String("\", \"program_name\": \"") + INFO_PROGRAM_NAME + 
                      String("\", \"major_version\": \"") + INFO_MAJOR_VERSION + 
                      String("\", \"minor_version\": \"") + INFO_MINOR_VERSION + 
                      String("\", \"build\": \"") + INFO_BUILD +
                      String("\", \"type\": \"") + INFO_BUILD_TYPE +
                      String("\", \"subtype\": \"") + INFO_BUILD_SUBTYPE +
                      String("\"}");
        return response(200, "text/plain", info);
      }
      if(function == "effect"){
        if(!findArg(args, "effect")) 
          return response(200, "text/plain", "No effect specified");
        effect_id = getArg(args, "effect");
        if(effect_id == "sinusoid"){
          randomSinusoid();
        }
        return response(200, "text/plain", "OK");
      }
      if(function == "effectSettings"){
        if(findArg(args, "hue")) sHue = getArg(args, "hue").toInt();
        if(findArg(args, "rainbow")) sRainbow = getArg(args, "rainbow").toInt();
        if(findArg(args, "speed")) sSpeed = getArg(args, "speed").toInt();
        if(findArg(args, "saturation")) sSaturation = getArg(args, "saturation").toInt();
        if(findArg(args, "chance")) sChance = getArg(args, "chance").toInt();
        if(findArg(args, "scale")) sScale = getArg(args, "scale").toDouble();
        return response(200, "text/plain", "OK");
      }
      if(function == "matrixSettings"){
        if(findArg(args, "brightness")) sBrightness = getArg(args, "brightness").toInt();
        return response(200, "text/plain", "OK");
      }
      if(function == "getEffectSettings"){
        String effectSettings = "{\"effect_id\":\""+effect_id+"\","+
                                "\"hue\":\""+String(sHue)+"\","+
                                "\"rainbow\":\""+String(sRainbow)+"\","+
                                "\"speed\":\""+String(sSpeed)+"\","+
                                "\"chance\":\""+String(sChance)+"\","+
                                "\"saturation\":\""+String(sSaturation)+"\","+
                                "\"scale\":\""+String(sScale)+"\"}";
        return response(200, "application/json", effectSettings);
      }
      if(function == "getMatrixSettings"){
        String matrixSettings = "{\"brightness\":"+String(sBrightness)+"}";
        return response(200, "text/plain", matrixSettings);
      }
    }
  }
  String m = "{\"status\": \"error\", \"message\": \"Not Found\", \"debug\": {\"path\": \""+path+"\", \"args\": {";
  for(char i = 0; i < args.getLength(); i++){
    m += "\"" + args.getByIndex(i).key + "\": \"" + args.getByIndex(i).data + "\"";
    if(i != args.getLength()-1)
      m += ", ";
  }
  m += "}}}";
  return response(404, "text/plain", m);
}

void handlePOST(AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total) {
  effect_id = "off";
  uint8_t* image = data;
  for(int i = 0; i < NUM_LEDS*3 && i < len; i+=3)
    drawPixelByIndex(i/3, CRGB(image[i], image[i+1], image[i+2]));
  FastLED.show();
  request->send(ApiResponse(request, response(200, "text/plain", "OK")));
}

String getArg(Vector<arg> args, String key){
  for(int i = 0; i < args.getLength(); i++)
    if(args.getByIndex(i).key == key)
      return args.getCurrent().data;
  return "";
}

bool findArg(Vector<arg> args, String key){
  for(int i = 0; i < args.getLength(); i++)
    if(args.getByIndex(i).key == key)
      return true;
  return false;
}

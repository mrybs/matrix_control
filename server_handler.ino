void handleGETApi() {
  LinkedList<arg> args;
  for (uint8_t i = 0; i < server.args(); i++) {
    args.Append(arg(server.argName(i), server.arg(i)));
  }
  response R = handleGET("/api", args);
  server.send(R.code, R.type, R.data);
}

void handlePOSTApi() {
  LinkedList<arg> args;
  for (uint8_t i = 0; i < server.args(); i++) {
    args.Append(arg(server.argName(i), server.arg(i)));
  }
  response R = handlePOST("/api", args);
  server.send(R.code, R.type, R.data);
}

void setBrightness(byte brightness){
  FastLED.setBrightness(MAX_BRIGHTNESS*brightness/39-2);
}

void handleGUI_index_html(){
  //server.send(200, "text/html", index_html);
  File f = SPIFFS.open("/index.html", "r");
  if(!f) return server.send(500, "plain/text", "Could not open file index.html");
  server.send(200, "text/html", f.readString().c_str());
  f.close();
}
void handleGUI_index_js(){
  //server.send(200, "text/javascript", index_js);
  File f = SPIFFS.open("/index.js", "r");
  if(!f) return server.send(500, "plain/text", "Could not open file index.js");
  server.send(200, "text/javascript", f.readString().c_str());
  f.close();
}
void handleGUI_styles_css(){
  //server.send(200, "text/css", styles_css);
  File f = SPIFFS.open("/styles.css", "r");
  if(!f) return server.send(500, "plain/text", "Could not open file styles.css");
  server.send(200, "text/css", f.readString().c_str());
  f.close();
}
void handleGUI_canvas_js(){
  //server.send(200, "text/javascript", canvas_js);
  File f = SPIFFS.open("/canvas.js", "r");
  if(!f) return server.send(500, "plain/text", "Could not open file canvas.js");
  server.send(200, "text/javascript", f.readString().c_str());
  f.close();
}

response handleGET(String path, LinkedList<arg> args){
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
        return response(200, "text/plain", String("NAME:") + INFO_NAME + 
                                          String(";ABOUT:") + INFO_ABOUT + 
                                          String(";PROGRAM_NAME:") + INFO_PROGRAM_NAME + 
                                          String(";MAJOR_VERSION:") + INFO_MAJOR_VERSION + 
                                          String(";MINOR_VERSION:") + INFO_MINOR_VERSION + 
                                          String(";BUILD:") + INFO_BUILD +
                                          String(";TYPE:") + INFO_BUILD_TYPE +
                                          String(";SUBTYPE:") + INFO_BUILD_SUBTYPE +
                                          String(";DEBUG:") + INFO_DEBUG);
      }
      if(function == "effect"){
        if(!findArg(args, "effect")) 
          return response(200, "text/plain", "No effect specified");
        effect_id = getArg(args, "effect");
        randomSinusoid();
        return response(200, "text/plain", "OK");
      }
      if(function == "effectSettings"){
        if(findArg(args, "hue")) sHue = getArg(args, "hue").toInt();
        if(findArg(args, "rainbow")) sRainbow = getArg(args, "rainbow").toInt();
        if(findArg(args, "speed")) sSpeed = getArg(args, "speed").toInt();
        if(findArg(args, "saturation")) sSaturation = getArg(args, "saturation").toInt();
        if(findArg(args, "chance")) sChance = getArg(args, "chance").toInt();
        if(findArg(args, "scale")) sScale = getArg(args, "scale").toDouble();
      }
      if(function == "matrixSettings"){
        if(findArg(args, "brightness")) sBrightness = getArg(args, "brightness").toInt();
      }
      if(function == "getEffectSettings"){
        return response(200, "application/json", "{\"effect_id\":\""+effect_id+"\","+
                                           "\"hue\":\""+String(sHue)+"\","+
                                           "\"rainbow\":\""+String(sRainbow)+"\","+
                                           "\"speed\":\""+String(sSpeed)+"\","+
                                           "\"chance\":\""+String(sChance)+"\","+
                                           "\"saturation\":\""+String(sSaturation)+"\","+
                                           "\"scale\":\""+String(sScale)+"\"}");
      }
      if(function == "getMatrixSettings"){
        return response(200, "text/plain", "{\"brightness\":"+String(sBrightness)+"}");
      }
      if(function == "getMatrix"){
        String image = "";
        for(int i = 0; i < NUM_LEDS; i++){
          CRGB pixel = getPixelByIndex(i);
          String r = String(pixel.r, HEX);
          String g = String(pixel.g, HEX);
          String b = String(pixel.b, HEX);
          if(r.length() == 1) r="0"+r;
          if(g.length() == 1) g="0"+g;
          if(b.length() == 1) b="0"+b;
          image += r;
          image += g;
          image += b;
        }
        return response(200, "text/plain", image);
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

response handlePOST(String path, LinkedList<arg> args){
  if(path == "/api"){
    if(findArg(args, "function")){
      String function = getArg(args, "function");
      if(function == "image"){
        String image = server.arg("plain");
        effect_id = "off";
        for(int i = 0; i < NUM_LEDS; i++)
          drawPixelByIndex(i, CRGB(
            Utils::stoh(String(image[i*8])+"0")*15 + Utils::stoh(String(image[i*8+1])+"0"),
            Utils::stoh(String(image[i*8+2])+"0")*15 + Utils::stoh(String(image[i*8+3])+"0"),
            Utils::stoh(String(image[i*8+4])+"0")*15 + Utils::stoh(String(image[i*8+5])+"0")
          ));
          FastLED.show();
        return response(200, "text/plain", "OK");
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

String getArg(LinkedList<arg> args, String key){
  for(int i = 0; i < args.getLength(); i++)
    if(args.getByIndex(i).key == key)
      return args.getCurrent().data;
  return "";
}

bool findArg(LinkedList<arg> args, String key){
  for(int i = 0; i < args.getLength(); i++)
    if(args.getByIndex(i).key == key)
      return true;
  return false;
}

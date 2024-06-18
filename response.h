struct response{
  int code;
  String type;
  String data;

  response(int code, String type, String data, size_t size = -1){
    this->code = code;
    this->type = type;
    this->data = data;
  }
};
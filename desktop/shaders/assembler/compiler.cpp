#include <fstream>
#include <iostream>
#include <algorithm> 
#include <cctype>
#include <locale>
#include <errno.h>

inline void ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {
        return !std::isspace(ch);
    }));
}
inline void rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
        return !std::isspace(ch);
    }).base(), s.end());
}

std::string remove_comments(const std::string& line){
    std::string n_line;
    for(auto c : line){
        if(c == ';') break;
        n_line += c;
    }
    return n_line;
}

int main(){
    std::ifstream mmss_fr; 
    mmss_fr.open("rainbow.mmss");
    if(!mmss_fr.is_open()){
        std::cout << "File could not be opened" << std::endl;
        return EIO;
    }
    std::ofstream mmss_fw;
    mmss_fw.open("rainbow.mmse", std::ios::binary);
    const char mmse_header[] = ({137, 77, 77, 83, 69, 13, 10, 0});
    mmss_fw.write(mmse_header, sizeof(mmse_header));
    std::string line;
    while(getline(mmss_fr, line)){
        line = remove_comments(line);
        rtrim(line);
        if(line.empty()) continue;
        std::cout << line << '\n';
    }
    mmss_fr.close();
    mmss_fw.close();
    return 0;
}
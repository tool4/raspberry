#include "stdio.h"
#include "stdlib.h"
#include <algorithm>
#include <cstring>
#include <iostream>
#include <sstream>

using namespace std;
std::string read_from_kbd();

int main(int argc, char* argv[])
{
    FILE *mplayer = NULL;
    unsigned int station_index = 0;
        
    unsigned int vol_level = 70;  // 70%
    bool ir_support = false;
    if(argc > 2)
    {
        if(strncmp(argv[1], "-ir", 3)==0)
        {
            ir_support = true;
        }
    }
    
    cout << "listening to " << (ir_support ? "IR" : "KBD") << endl;

    std::string str = "";
    
    while (true)
    {
        str = "";

        if( ir_support)
        {
            cin >> str;
        }
        else
        {
            str = read_from_kbd();
        }
    
        if (str.size())
        {
	    std::cout << "STR: "<< str << "\n";
            if(str == "up" ||
               str == "down" ||
               str == "left" ||
               str == "right" ||
               str == "vol_up" ||
               str == "vol_down" ||
               str == "menu" ||
               str == "exit" ||
               str == "zoom" ||
               str == "slideshow" ||
               str == "enter")
            {
                std::cout << str << "\n";
                if(str == "enter")
                {
                    if (mplayer)
                    {
                        pclose(mplayer);
                    }
                    std::string cmdline = "mplayer -nocache -afm ffmpeg http://stream3.polskieradio.pl:8904";
                    cout << "playing: " << cmdline.c_str() << endl;
                    mplayer = popen(cmdline.c_str(), "r");
                }
                else if (str == "right")
                {
                    if (mplayer)
                    {
                        pclose(mplayer);
                    }
                    std::string cmdline = "mplayer -nocache -afm ffmpeg ";
                    std::stringstream station;
                    std::stringstream cmdss;
                    station_index++;
                    station << "http://stream.open.fm/" << station_index;
                    cmdss << cmdline << station.str();
                        
                    cout << "playing: " << station.str() << endl;
                    cout << "playing: " << cmdss.str().c_str() << endl;
                    mplayer = popen(cmdss.str().c_str(), "r");
                }
                else if (str == "left")
                {
                    if (mplayer)
                    {
                        pclose(mplayer);
                    }
                    std::string cmdline = "mplayer -nocache -afm ffmpeg ";
                    std::stringstream station;
                    std::stringstream cmdss;
                    if(station_index>1)
                        station_index--;
                    station << "http://stream.open.fm/" << station_index;
                    cmdss << cmdline << station.str();
                        
                    cout << "playing: " << cmdss.str().c_str() << endl;
                    mplayer = popen(cmdss.str().c_str(), "r");
                }
                else if (str == "vol_up")
                {
                    if(vol_level < 100)
                    {
                        vol_level += 1;
                        std::stringstream cmdss;
                        cmdss << "amixer  sset PCM,0 ";
                        cmdss << vol_level << "% > /dev/null";
                        std::cout << cmdss.str().c_str() << std::endl;
                        system(cmdss.str().c_str());
                    }
                }
                else if (str == "vol_down")
                {
                    if(vol_level > 0)
                    {
                        vol_level -= 1;
                        std::stringstream cmdss;
                        cmdss << "amixer  sset PCM,0 ";
                        cmdss << vol_level << "% > /dev/null";
                        std::cout << cmdss.str().c_str() << std::endl;
                        system(cmdss.str().c_str());
                    }
                }
                else if(str == "exit")
                {
                    if (mplayer)
                    {
                        pclose(mplayer);
                    }
                }
            }
        }
    }
    return 0;
}

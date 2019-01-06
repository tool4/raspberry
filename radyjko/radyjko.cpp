#include "stdio.h"
#include <algorithm>
#include <iostream>
#include <sstream>

//#define IR_SUPPORT 0
#define KBD_SUPPORT 1

std::string read_from_kbd();

int main(void)
{
    unsigned int vol_level = 70;  // 70%
    while (true)
    {
        std::string str;
#ifdef KBD_SUPPORT
        str = read_from_kbd();
#else
        std::cin >> str;
#endif
        if (str.size())
        {
            //std::cout << str << "\n";
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
                    //system("bash mplayer -nocache -afm ffmpeg "
                    //"http://stream3.polskieradio.pl:8904 > /dev/null");
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
            }
        }
    }
    return 0;
}

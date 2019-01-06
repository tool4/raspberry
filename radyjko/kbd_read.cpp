#include "stdio.h"
#include <iostream>

#include <unistd.h>
#include <termios.h>

char getch()
{
    char buf = 0;
    struct termios old = {0};
    if (tcgetattr(0, &old) < 0)
        perror("tcsetattr()");
    old.c_lflag &= ~ICANON;
    old.c_lflag &= ~ECHO;
    old.c_cc[VMIN] = 1;
    old.c_cc[VTIME] = 0;
    if (tcsetattr(0, TCSANOW, &old) < 0)
        perror("tcsetattr ICANON");
    if (read(0, &buf, 1) < 0)
        perror ("read()");
    old.c_lflag |= ICANON;
    old.c_lflag |= ECHO;
    if (tcsetattr(0, TCSADRAIN, &old) < 0)
        perror ("tcsetattr ~ICANON");
    return (buf);
}

std::string read_from_kbd()
{
    std::string str;
    char c = getch();
    switch(c)
    {
    case 'w':  str = "up";        break;
    case 's':  str = "down";      break;
    case 'a':  str = "left";      break;
    case 'd':  str = "right";     break;
    case '\n': str = "enter";     break;
    case 27:   str = "exit";      break;
    case '+':  str = "vol_up";    break;
    case '-':  str = "vol_down";  break;
    case 'm':  str = "menu";      break;
    case 'z':  str = "zoom";      break;
    case ' ':  str = "slideshow"; break;
    //default: printf("pressed %d [%c]\n", c, c); break;
    }
    return str;
}

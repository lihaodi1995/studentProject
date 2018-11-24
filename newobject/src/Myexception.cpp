#include "Myexception.h"
#include<exception>
Myexception::Myexception(Extype a)
{
        exceptiontype = a;
}

Myexception::~Myexception()
{
        //dtor
}
const char* Myexception::what() const throw(){
        switch((int) exceptiontype)
        {
                case 1: return "DATE_INVALID";
                case 2: return "RANGE_INVALID";
                case 3: return "SCORE_INVALID";
                case 4: return "INPUT_INVALID";
                default: break;
        }
        return "\0";
}

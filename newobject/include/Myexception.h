#ifndef MYEXCEPTION_H
#define MYEXCEPTION_H

#include <exception>
using namespace std;
enum Extype{DATE_INVALID = 1, RANGE_INVALID = 2, SCORE_INVALID = 3, INPUT_INVALID = 4};
class Myexception: public exception
{
        public:
                Myexception(Extype );
                virtual ~Myexception();
                virtual const char* what() const throw();
        private:
                Extype exceptiontype;
};

#endif // MYEXCEPTION_H

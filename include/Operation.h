#include"Student.h"
#include"Date.h"
#include"Course.h"
#ifndef OPERATION_H
#define OPERATION_H


class Operation
{
        public:
                Operation();
                virtual ~Operation();
        private:
                Student* init();
                void ope();
                void addocourse();
                void addecourse();
                void removecourse();
                void print();
                void exitope();
                void setcourse();
                void check();
                void checks();
                void menu();
                Student* student;
                int obnum;
                int elnum;
};

#endif // OPERATION_H

#include "..\include\Course.h"
#include<string>
#include<iostream>
#include<exception>
#include<typeinfo>
using namespace std;
Course::Course(const string a, const int b)
{
        setcourse(a, b);
}

Course::~Course(){
        name.clear();
}

int Course::getmax(){
        return creditHour;
}

void Course::setcourse(const string a, const int b){
        name = getname(a);
        creditHour = gethour(b);
}

string Course::getname(const string a){
        string temp = a;
        return temp;
}

string Course::returnname(){
        return name;
}

int Course::gethour(const int a){
        int temp = a;
        return temp;
}

double Course::getscore(){
        return (double)creditHour;
}

ostream& operator <<(ostream& otput, Course a){
        otput<<"Coursename: "<<a.name<<" score: "<<a.getscore();
        return otput;
}

ObligatoryCourse::ObligatoryCourse(const string a, const int b, const int c):Course(a, b){
        setob(c);
}

ObligatoryCourse::ObligatoryCourse(const Course a, const int b):Course(a){
        setob(b);
}

ObligatoryCourse::ObligatoryCourse(){

}

ObligatoryCourse::~ObligatoryCourse(){

}

void ObligatoryCourse::setob(const int a){
        mark = a;
}

double ObligatoryCourse::getscore(){
        double temp = mark;
        return temp;
}

ElectiveCourse::ElectiveCourse(const string a, const int b, const char c):Course(a, b){
        string d = "ElectiveCourse";
        setel(c);
}

ElectiveCourse::ElectiveCourse(){

}

ElectiveCourse::ElectiveCourse(const Course a, const char b):Course(a){
        setel(b);
}

ElectiveCourse::~ElectiveCourse(){

}
void ElectiveCourse::setel(const char a){
        grade = a;
}

double ElectiveCourse::getscore(){
        double temp;
        temp = 745 - 10 * (int)grade;
        return temp;
}

char ElectiveCourse::getgrade(){
        char temp;
        temp = grade;
        return temp;
}

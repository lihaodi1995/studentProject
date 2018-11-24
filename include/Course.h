#ifndef COURSE_H
#define COURSE_H
#include<string>
#include<iostream>
using namespace std;

class Course
{
        public:
                Course(const string = NULL, const int = 0);
                ~Course();
                string getname(const string);
                string returnname();
                int gethour(const int);
                void setscore(const int);
                int getmax();
                void setcourse(const string, const int);
                friend ostream& operator <<(ostream&, Course);
                virtual double getscore();
        private:
                int creditHour;
                string name;
};

class ObligatoryCourse :public Course
{
        public:
                ~ObligatoryCourse();
                ObligatoryCourse();
                ObligatoryCourse(const string, const int = 0, const int = 0);
                ObligatoryCourse(const Course, const int = 0);
                void setob(const int);
                virtual double getscore();
        private:
                int mark;
};

class ElectiveCourse :public Course
{
        public:
               ElectiveCourse(const string, const int = 0, const char = 'E');
               ElectiveCourse(const Course, const char = 'E');
               ElectiveCourse();
               ~ElectiveCourse();
               void setel(const char);
               virtual double getscore();
               char getgrade();
        private:
                char grade;
};
#endif // COURSE_H

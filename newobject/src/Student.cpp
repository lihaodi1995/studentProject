#include<string.h>
#include<iostream>
#include"..\include\Date.h"
#include"..\include\Course.h"
#include "..\include\Student.h"
#include"..\include\Myexception.h"
#include<exception>
#include<sstream>
#include<fstream>
#include<typeinfo>
using namespace std;

int Student::count = 0;

Student::Student(const char * const input, int y, int m, int d):birthdate(y, m ,d)
{
	name = new char[strlen(input) + 1];
	for(int i = 0 ; i <  MAX_SIZE; i++){
                Courselist[i] = NULL;
	}
	strcpy(name,input);
	coursenum = 0;
	count++;
	readin();
}

/*Student::Student(const Student &a):birthdate(a.birthdate)
{
	name = new char[strlen(a.name) + 1];
	for(int i = 0 ; i <  MAX_SIZE; i++){
                Courselist[i] = NULL;
	}
	strcpy(name, a.name);
	coursenum = 0;
	count++;
}

Student::Student(const char * const input, const Date &a):birthdate(a)
{

	name = new char[strlen(input) + 1];
	for(int i = 0 ; i <  MAX_SIZE; i++){
                Courselist[i] = NULL;
	}
	strcpy(name, input);
	coursenum = 0;
	count++;
}
*/
Student::~Student()
{
	delete []name;
	for(int i = 0 ; i <  MAX_SIZE; i++){
                Courselist[i] = NULL;
	}
	count--;
}

void Student::printdate()const{
        Student::birthdate.studentprint();
}

void Student::printname()const{
        cout<<Student::name<<endl;
}

int Student::getcoursenum() const{
        return coursenum;
}

void Student::getbirthday(int &a, int &b, int &c)const{
        a = Student::getyear();
        b = Student::getmonth();
        c = Student::getday();
}

int Student::getyear()const{
        return Student::birthdate.sendyear();
}

int Student::getmonth()const{
        return Student::birthdate.sendmonth();
}

int Student::getday()const{
        return Student::birthdate.sendday();
}

void Student::printcount(){
        std::cout<<Student::count<<endl;
}

bool Student::removecourse(const int i){
        if(i > coursenum || i <= 0) return false;
        if(Courselist[i - 1]) Courselist[i - 1] = NULL;
        if(coursenum > 0)coursenum--;
        readin();
        return true;
}

void Student::setcourse(int place){
        if(place < 1 || place > MAX_SIZE || place > coursenum) throw Myexception(RANGE_INVALID);
        cout<<*Courselist[place - 1]<<endl;
        if(typeid(*Courselist[place - 1]) == typeid(ObligatoryCourse)){
                int a;
sotag:
                try{
                        cout<<"Please input the mark.\n";
                        cin>>a;
                        if(cin.good() == 0) throw Myexception(INPUT_INVALID);
                        else if(a < 0 || a > 100) throw Myexception(SCORE_INVALID);
                }
                catch(Myexception ex){
                        cout<<"error: "<<ex.what()<<"\n";
                        goto sotag;
                }
                dynamic_cast<ObligatoryCourse*>(Courselist[place - 1])->setob(a);
        }
        else{
                char b;
setag:
                try{
                        cout<<"Please input the grade.\n";
                        cin>>b;
                        if((int)b <65 || (int) b > 69) throw Myexception(SCORE_INVALID);
                        else if(cin.good() == 0) throw Myexception(INPUT_INVALID);
                }
                catch(Myexception ex){
                        cout<<"error: "<<ex.what()<<"\n";
                        goto setag;
                }
                dynamic_cast<ElectiveCourse*>(Courselist[place - 1])->setel(b);
        }
        readin();
}

double Student::getscore(int a){
        if(a >= 0 && Courselist[a]){
                if(typeid(*Courselist[a]) == typeid(ObligatoryCourse)) cout<<dynamic_cast<ObligatoryCourse*>(Courselist[a])->getscore();
                else cout<<dynamic_cast<ElectiveCourse*>(Courselist[a])->getgrade();
        }
        cout<<"\n";
        return 0;
}

string Student::getcoursename(int a){
        return Courselist[a]->returnname();
}

double Student::calcredict(){
        double sum1 = 0, sum2 = 0, sum3 = 0, sum4 = 0, sum = 0;
        for(int i = 0; i < coursenum; i++){
                if(typeid(*Courselist[i]) == typeid(ObligatoryCourse)){
                        sum1 += Courselist[i]->getscore() * Courselist[i]->getmax() ;
                        sum3 += Courselist[i]->getmax();
                }
                else if(typeid(*Courselist[i]) == typeid(ElectiveCourse)){
                        sum2 += Courselist[i]->getscore();
                        sum4 ++;
                }
        }
        if(sum3 > 0) sum += 0.6 * sum1 / sum3;
        if(sum4 > 0) sum += 0.4 * sum2 / sum4;
        return sum;
}
Student* Student::addCourse(Course *course){
        Course* temp = course;
        Courselist[coursenum] = temp;
        coursenum ++;
        readin();
        return this;
}

void Student::readin(){
        string dn(name);
        dn += ".txt";
        fstream store(dn, ios::out);
        store<<*this;
        store.close();
}
/*
Student* Student::addCourse(const string a, const int b){
        if(coursenum == MAX_SIZE) return this;
        Course *temp = new Course(a, b);
        Courselist[coursenum] = temp;
        coursenum ++;
        return this;
}
*/
ostream& operator << (ostream& otput, Student& a){
        otput<<"Name: "<<a.name<<" Birthdate: "<<a.birthdate<<"There are "<<a.coursenum<<" courses.\n";
        for(int i = 0; i < a.coursenum; i++){
                otput<<i+1<<": "<<*(a.Courselist[i]);
                if(typeid(*(a.Courselist[i])) == typeid(ObligatoryCourse)) otput<<" mark: "<<dynamic_cast<ObligatoryCourse*>(a.Courselist[i])->getscore();
                else if(typeid(*(a.Courselist[i])) == typeid(ElectiveCourse)) otput<<" grade: "<<dynamic_cast<ElectiveCourse*>(a.Courselist[i])->getgrade();
                otput<<endl;
        }
        return otput;
}




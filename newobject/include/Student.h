#ifndef STUDENT_H
#define STUDENT_H
#include"Date.h"
#include"Course.h"
#define MAX_SIZE 25
#include<iostream>
using namespace std;
class Student
{
	public:
		Student(const char * const input, int y, int m, int d);
		Student( const Student &a);
		Student(const char* const input, const Date &a);
		~Student();
		void setdate(int , int , int)const;
		void printdate() const;
		void printname() const;
		void getbirthday(int &a, int &b, int &c)const;
		int getday() const;
		int getmonth() const;
		int getyear() const;
		int getcoursenum() const;
		char* getname(char *);
		void setname(char *);
		void printcount();
		bool removecourse(const int );
		double calcredict();
		void setcourse(int);
		void readin();
		double getscore(int);
		string getcoursename(int );
		Student* addCourse(Course*);
		Student* addCourse(const string,const int );
		friend ostream& operator << (ostream&, Student&);
	private:
		char *name;
		int length;
		static int count;
		const Date birthdate;
		Course* Courselist[MAX_SIZE];
		int coursenum;
};
#endif

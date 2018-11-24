#ifndef TIME_H
#define TIME_H
#include<iostream>
using namespace std;
class Date
{
public:
	Date();
	Date(int, int, int);
	Date(const Date&);
	~Date();
	int getyear(int)const ;
	int getmonth(int)const ;
	int getday(int)const ;
	int sendyear()const;
	int sendmonth()const;
	int sendday()const;
	void setDate(int,int,int );
	void nextDay();
	bool isLeapYear(int );
	bool check(int, int, int );
	void studentprint()const;
	void print()const;
	Date operator ++();
	Date operator ++(int);
	friend ostream& operator <<(ostream&, const Date);
private:
	int day;
	int month;
	int year;
};
#endif




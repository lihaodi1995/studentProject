#include<iostream>
#include"..\include\Date.h"
#include<stdlib.h>
#include"..\include\Myexception.h"
using namespace std;
int days1[12] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
int days2[12] = { 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

Date::Date(){
	Date::setDate(1, 1, 1);
}

Date::Date(int y ,int m, int d){
	Date::setDate(y, m, d);
}

Date::Date(const Date &D){
	day = D.day;
	month = D.month;
	year = D.year;
}

Date::~Date(){
}
int Date::getday(int d)const {
	return d;
}

int Date::getyear(int y)const {
	return y;
}

int Date::getmonth(int m)const {
	return m;
}

int Date::sendyear()const{
	return Date::year;
}

int Date::sendmonth()const{
	return Date::month;
}

ostream& operator <<(ostream& otput, const Date a){
        otput<<a.year<<" "<<a.month<<" "<<a.day<<endl;
        return otput;
}


int Date::sendday()const{
	return Date::day;
}

void Date::setDate(int y,int m,int d)
{
	year = Date::getyear(y);
	month = Date::getmonth(m);
	day = Date::getday(d);
	if(Date::check(year, month, day) == false) throw Myexception(DATE_INVALID);
}

bool Date::check(int y, int m, int d){
	if((y <= 0)||( m <= 0)||( m > 12) || (y <= 0)||( d > (Date::isLeapYear(y)? days2[month - 1] : days1[month - 1]))){
		return false;
	}
	return true;
}

bool Date::isLeapYear(int y){
	if(y % 4 == 0 && ( y % 400 == 0 || y % 100 != 0)) return true;
	else return false;
}

void Date::nextDay(){
	day++;
	if(Date::isLeapYear(year)){
		if( day > days2[month - 1]){
			day -= days2[month - 1];
			month++;
		}
	}
	else{
		if( day > days1[month - 1]){
			day -= days1[month - 1];
			month++;
		}
	}
	if(month > 12){
		month -= 12;
		year++;
	}
}

void Date::print()const{
	cout<<year<<"-"<<month<<"-"<<day<<"-"<<endl;
}

void Date::studentprint()const{
        cout<<"his birthdate is "<<year<<" year "<<month<<" month "<<day<<" day "<<endl;
};

Date Date::operator++(){
        Date::nextDay();
        return *this;
}

Date Date::operator++(int){
        Date temp(*this);
        Date::nextDay();
        return temp;
}

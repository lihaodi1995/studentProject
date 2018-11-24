#include "..\include\Operation.h"
#include"..\include\Date.h"
#include"..\include\Student.h"
#include"..\include\Course.h"
#include"..\include\Myexception.h"
#include<iostream>
#include<stdlib.h>
#include<fstream>
#include<sstream>
#define MAX_SIZE 25
using namespace std;

Operation::Operation()
{
        student = init();
        ope();
}

void Operation::ope(){
        int in;
optag:
        try{
                menu();
                cin>>in;
                if(cin.good() == 0) throw Myexception(INPUT_INVALID);
                else if(in < 1 || in > 8) throw Myexception(RANGE_INVALID);
        }
        catch(Myexception ex){
                cout<<"Error: "<<ex.what()<<"\n";
                system("cls");
                goto optag;
        }
        if(in == 1) addocourse();
        else if(in == 2) addecourse();
        else if(in == 3) removecourse();
        else if(in == 4) print();
        else if(in == 5) setcourse();
        else if(in == 6) check();
        else if(in == 7) checks();
        else if(in == 8) exitope();
        else cout<<"invalid operation.\n";
        system("pause");
        system("cls");
        ope();
}
Student* Operation::init(){
bg:
        cout<<"Welcome to use course choosing system.\nPlease input student's name.\nOr you can input a string with the bdeginning of '0' to build from txt document.\n";

        char *name = new char[30];
        static Student* test;
        int y, m, d;
        cin>>name;
        if(name[0] == '0'){
                cout<<"now let's input the document name. Don't forget to add '.txt'\n";
                string dn;
                cin>>dn;
                fstream ns;
                ns.open(dn, ios::in);
                if(!ns){
                    cout<<"the document doesn't exist. Try again\n";
                    goto  bg;
                }
                else{
                    string coursename, rubbish;
                    char grade;
                    int score, ey, em, ed, mark;
                    char *ename = new char[30];
                    ns>>rubbish>>ename>>rubbish>>ey>>em>>ed;
                    test = new Student(ename, ey, em, ed);
                    ns>>rubbish;
                    getline(ns, rubbish);
                    while(ns>>rubbish>>rubbish>>coursename>>rubbish>>score){
                        ns>>rubbish;
                        if(rubbish[0] == 'm'){
                                ns>>mark;
                                ObligatoryCourse* no = new ObligatoryCourse(coursename, score, mark);
                                test->addCourse(no);
                        }
                        else{
                                ns>>grade;
                                ElectiveCourse* ne = new ElectiveCourse(coursename, score, grade);
                                test->addCourse(ne);
                        }
                    }
                }
        }

        else{
                Date temp;
datetag:
               try{
                        cout<<"Please input his birthdate.\n";
                        cin>>y>>m>>d;
                        if(cin.good() == 0) throw Myexception(INPUT_INVALID);
                        else if(temp.check(y, m, d) == false) throw Myexception(DATE_INVALID);
               }
               catch(Myexception ex){
                        cout<<"Error: "<<ex.what()<<"\n";
                        goto datetag;
               }
                test = new Student(name, y, m, d);
        }
        return test;
}

void Operation::check(){
        cout<<student->calcredict()<<"\n";
}

void Operation::addocourse(){
        if(student->getcoursenum() >= MAX_SIZE){
                cout<<"invaild operation.\n";
                return ;
        }
        cout<<"Here are the courselist.\n";
        fstream index("OB.txt", ios::in);
        string in;
        obnum = 0;
        while(getline(index, in))
        {
                cout<<in<<endl;
                obnum++;
        }
        string id;
        int realid;
        stringstream trans;
obtag:
        try{
                cout<<"Please input the course id.\n";
                cin>>id;
                trans.clear();
                trans<<id;
                trans>>realid;
                if(realid > obnum || realid < 1) throw Myexception(RANGE_INVALID);
        }
        catch(Myexception ex){
                cout<<"error: "<<ex.what()<<"\n";
                goto obtag;
        }
        fstream choose("OB.txt", ios::in);
        while(getline(choose, in))
        {
                if(in[0] == id[0])
                {
                        int b, t;
                        int l = in.length();
                        for(b = 0; b < l; b++)
                                if(in[b] == '.') break;
                        for(t = b + 1; t < l; t++)
                                if(in[t] == ' ') break;
                        string name(&in[b + 1], &in[t]);
                        string temp(in, t + 1);
                        int score;
                        trans.clear();
                        trans<<temp;
                        trans>>score;
                        ObligatoryCourse* noc = new ObligatoryCourse(name, score);
                        student->addCourse(noc);
                }
        }
        return;
}

void Operation::addecourse(){
        if(student->getcoursenum() >= MAX_SIZE){
                cout<<"invaild operation.\n";
                return ;
        }
        cout<<"Here are the courselist.\n";
        fstream index("EL.txt", ios::in);
        string in;
        elnum = 0;
        while(getline(index, in))
        {
                cout<<in<<endl;
                elnum++;
        }
        string id;
        int realid;
        stringstream trans;
eltag:
        try{
                cout<<"Please input the course id.\n";
                cin>>id;
                trans.clear();
                trans<<id;
                trans>>realid;
                if(realid > elnum || realid < 1) throw Myexception(RANGE_INVALID);
        }
        catch(Myexception ex){
                cout<<"error: "<<ex.what()<<"\n";
                goto eltag;
        }
        fstream choose("EL.txt", ios::in);
        while(getline(choose, in))
        {
                if(in[0] == id[0])
                {
                        int b, t, l = in.length();
                        for(b = 0; b < l; b++)
                                if(in[b] == '.') break;
                        for(t = b + 1; t < l; t++)
                                if(in[t] == ' ') break;
                        string name(&in[b + 1], &in[t]);
                        string temp(in, t + 1);
                        int score;
                        stringstream trans;
                        trans.clear();
                        trans<<temp;
                        trans>>score;
                        ElectiveCourse* nec = new ElectiveCourse(name, score);
                        student->addCourse(nec);
                }
        }
}

void Operation::removecourse(){
        int i;
rctag:
        try{
                cin>>i;
                cout<<"Please input its place.\n";
                if(cin.good() == 0) throw Myexception(INPUT_INVALID);
                if(student->removecourse(i) == false) throw Myexception(RANGE_INVALID);
        }
        catch(Myexception ex){
                cout<<"error: "<<ex.what()<<"\n";
                goto rctag;
        }
}

void Operation::menu(){
        cout<<"You can input:\n1 to add obligatorycourse.\n2 to add electivecourse.\n3 to remove course.\n4 to print student data.\n5 to set course score.\n6 to check gpa.\n7 to check one score.\n8 to exit.\nPlease input your operation.\n";
}

void Operation::print(){
        cout<<*student;
}

void Operation::exitope(){
        exit(0);
}

void Operation::setcourse(){
        int place;
sctag:
        try{
                cout<<"Please input its id.\n";
                cin>>place;
                if(cin.good() == 0) throw Myexception(INPUT_INVALID);
        }
        catch(Myexception ex){
                cout<<"error: "<<ex.what()<<"\n";
                goto sctag;
        }
        student->setcourse(place);
}

void Operation::checks(){
        int id;
cctag:
        try{
                cout<<"Please input the course id.\n";
                cin>>id;
                if(cin.good() == 0) throw Myexception(INPUT_INVALID);
        }
        catch(Myexception ex){
                cout<<"error: "<<ex.what()<<"\n";
                goto cctag;
        }
        student->getscore(id - 1);
}

Operation::~Operation()
{
        //dtor
}



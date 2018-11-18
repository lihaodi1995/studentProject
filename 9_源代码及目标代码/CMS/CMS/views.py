from django.shortcuts import render	
def base(request):
    return render(request,'base.html')

def login(request):
    return render(request,'login.html')

def user_register(request):
	return render(request,'user_register.html')

def institution_register(request):
	return render(request,'institution_register.html')
from django.http import HttpResponseRedirect
from login.models import Account , User, statement
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login
from django.db import IntegrityError


def Home(request):
    return render(request,"Bank.html")


def newAccount(request):
    data = {"pass":None,"Account":'',"Acc_no":'',"name":None, "link":None, "url":None, "pin":None}

    try : 
        print("newAccount")
        if request.method == "POST":

                name = request.POST["User"]
                password = request.POST["password"]
                confirm_password = request.POST['confirm_password']
                Mobile = request.POST["Mobile_no"]

                if password == confirm_password:
                    print("!1")
                    try:
                        print("!2")
                        user = User.objects.create_user(username=name, password=password)
                        user.save()

                    except IntegrityError:
                        
                        data = {"pass":None,"Account":"Username already taken.","Acc_no":'',"name":''}
                        return render(request, "open_Acc.html",data)
                    
                    print("!3")
                    print('user',user)
                    record = Account(user_name=user, Mobile_no=Mobile)
                    record.save()
                    user.first_name = user.username
                    user.username = f'{1201100+record.id}'
                    user.save()
                    print("first",user.first_name)
                    print('username',user.username)
                    print("!4")
                    Balance = 2000
                    transfer = 2000
                    Result = statement(user,Balance,transfer,"Deposit")
                    
                        
                    print("record",record.user_name)
                    login(request, user)
                    print("success")
                    return HttpResponseRedirect(reverse('LoginApp:account'))
            
    except : 
        data["Acc_no"] = "Something Wrong !!!"   
        return render(request,"open_Acc.html",data)


    return render(request,"open_Acc.html",data)


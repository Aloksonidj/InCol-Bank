from django import forms
from login.models import Account as acc
from django.shortcuts import redirect, render

class openAccount(forms.Form):
    
    User = forms.CharField(label="User name",max_length=64,required=True ,label_suffix="")

    password = forms.CharField(label="Password",max_length=20,min_length=6,required=True)

    Mobile_no = forms.IntegerField(label="Mobile_no",required=True)



def Home(request):
    return render(request,"Bank.html")


def newAccount(request):
    data = {"pass":None,"Account":'',"Acc_no":'',"name":None, "link":None, "url":None, "pin":None}

    try : 

        if request.method == "POST":

                name = request.POST["User"]
                password = request.POST["password"]
                Mobile = request.POST["Mobile_no"]

                acc(user_name=name, passwords=password, Mobile_no=Mobile, balance=2000, status="Active", pin=None).save()
                Id = acc.objects.get(user_name=name)

                data = {"pass":None,"Account":"Your Account No is","Acc_no":Id.id,"name":Id.user_name}
                return render(request, "open_Acc.html", data)

    except : 
        data["Acc_no"] = "Something Wrong !!!"   
        return render(request,"open_Acc.html",data)


    return render(request,"open_Acc.html",data)


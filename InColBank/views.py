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

    if request.method == "POST":
        print(request.POST)

        form = openAccount(request.POST)

        if form.is_valid():

            name = form.cleaned_data["User"]
            password = form.cleaned_data["password"]
            Mobile = form.cleaned_data["Mobile_no"]

            acc(user_name=name, passwords=password, Mobile_no=Mobile, balance=2000, status="Active", pin=None).save()
            Id = acc.objects.get(user_name=name)

            data = {"form":openAccount(),"pass":None,"Account":"Your Account No is","Acc_no":Id.id,"name":Id.user_name}
            return render(request, "open_Acc.html", data)
        
        else:

            Form = {"form":openAccount(),"Account":"Something Gone Wrong","Acc_no":"Please try Again"}
            return render(request,"open_Acc.html",Form)
    
    Form = {"form":openAccount()}
    return render(request,"open_Acc.html",Form)


from django.shortcuts import render
from .models import Account as Acc

# Create your views here.
def Login(request):
    data = {"name":None,"link":None,"url":None,"pin":None}

    count = 0
    
    if count > 0:

        if request.method == "POST":

            Account_no = int(request.POST["Account_no"])
            Passwrd = request.POST["password"]


            Account=Acc.objects.get(id=Account_no)

            if Account.id == Account_no and Passwrd == Account.passwords:
                
                data["pass"] = "Login Successfull....."
                data["name"] = Account.user_name

                return render(request,"login/Login.html",data)

    return render(request,"login/Login.html")


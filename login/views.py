from django.http import HttpResponse ,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Account as Acc
from django.contrib.auth import authenticate, login, logout

# Create your views here.

#To Login In Existing Account
def Login(request):

    #To Give Addition Info     
    data = {"name":None,"link":None,"url":"","pin":None}

    #TO Check Form Submition 
    if request.method == "POST":

        #Get Information From Form
        Account_no = request.POST["Account_no"]
        Passwrd = request.POST["password"]

        try:

            user = authenticate(request, username=Account_no, password=Passwrd)

            if user is not None:
                login(request, user)

                #Getting Account Detail According To Account No Given IN Form
                return HttpResponseRedirect(reverse('account', args=(Account_no,)))
             
            else: 
                data['pass'] = "InValid Username And PassWord!!!"
                return render(request,"login/Login.html", data)
            
        except :
            data['pass'] = "This Account Does Not Exist!!!"
            return render(request,"login/Login.html", data)

    return render(request,"login/Login.html", data)



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("Home"))


#To Display Account Detail After Login 
def accountDetail(request,acc):
    print("acc",acc)
    print(type(acc))

    Account = Acc.objects.get(id = acc)
    data = {"name":Account.user_name,"link":None,"url":"","pin":Account.pin,"Detail":Account}

    if Account :
        return render(request,"login/account.html", data)

    return render(request,"login/account.html")



# def moneyTransfer(request,id=1201107):

#     data = {"name":None,"link":None,"url":"","pin":None}
#     # id = request.session.get['Id']

#     try:
#             Account = Acc.objects.get(id = id)
#             print("Account",Account.user_name)
#             Balance = Account.balance
#             print("Balance",Balance)
#             data['name'] = Account.user_name
#             data['Amount'] = Balance

#             if request.method == "POST" :
#                 print("1!")

#                 Beni_acc_no = int(request.POST["Beneficiary"])
#                 print("Acc_no",Beni_acc_no)

#                 Beni_account = None

#                 some = Acc.objects.all()

#                 for account in some : 

#                     if account.id == Beni_acc_no :

#                         Beni_account = Acc.objects.get(id = Beni_acc_no)

#                 if Beni_account :

#                     print("Beni_Account",Beni_account)

#                     transfer = int(request.POST['transfer'])
#                     print("transfer",transfer)

#                     if transfer > 0 :
#                         print("some")

#                         if Balance >= transfer :
#                             print("3!")

#                             Account.balance = Account.balance - transfer

#                             if Account.balance >= 0 :

#                                 Account.save()
#                                 Balance = Account.balance
#                                 print("Acc",Account.balance)
#                                 Beni_account.balance = Beni_account.balance + transfer
#                                 Beni_account.save()
#                                 print("Beni",Beni_account.balance)

#                                 data["Amount"] = Balance
#                                 data['transfer'] = "Transition Successfull!!!!!"

#                                 return render(request,"login/user.html",data)
                            
#                             else : 
#                                 data["Amount"] = Balance
#                                 data['transfer'] = "Your Balance Is Zero 0"
#                                 return render(request,"login/user.html",data)
                        
#                         else : 

#                             data['transfer'] = "Inefficient Balance"
#                             return render(request,"login/user.html",data)
                
#                     else: 

#                         data['transfer'] = "Enter 1 or more "
#                         return render(request,"login/user.html",data)
                    
#                 else : 
#                     data['transfer'] = "Beneficiary Does Not Exist !!!!"
#                     return render(request,"login/user.html",data)

#     except :
#             data['tranfer'] = "Error"
#             return render(request,"login/user.html",data)
    
#     return render(request,"login/user.html",data)
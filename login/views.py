from django.http import HttpResponse ,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Account as Acc, statement as state
from django.contrib.auth import authenticate, login, logout

# Create your views here.

#To Login In Existing Account
def Login(request):

    #To Give Addition Info     
    data = {"name":None,"link":None,"url":"","pin":None}

    #TO Check Form Submition 
    if request.method == "POST":

        #Get Information From Form
        Account_no = str(request.POST["Account_no"])
        Passwrd = request.POST["password"]

        try:
            user = authenticate(request, username=Account_no, password=Passwrd)

            if user is not None:

                login(request, user)
                id = int(Account_no)-1201100

                #Getting Account Detail According To Account No Given IN Form
                return HttpResponseRedirect(reverse('LoginApp:account', args=(id,)))
             
            else: 
                data['pass'] = "InValid Username And PassWord!!!"
                return render(request,"login/Login.html", data)
            
        except :
            data['pass'] = "This Account Does Not Exist!!!"
            return render(request,"login/Login.html", data)

    return render(request,"login/Login.html", data)


#To LogOut 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("Home"))



#To Display Account Detail After Login 
def accountDetail(request,acc):

    Account = Acc.objects.get(id = acc)
    data = {"name":Account.user_name,"link":reverse("LoginApp:logout"),"url":"Logout","pin":Account.pin,"Detail":Account}

    if Account :
        return render(request,"login/account.html", data)

    return render(request,"login/account.html")


#To Deposit Money In Self Account Or Transfer Money To Other's Account
def moneyTransfer(request,id):

    data = {"name":"Hello","link":reverse("LoginApp:logout"),"url":"Logout","pin":None}
    Account_no = int(id)-1201100
    print(id)

    try:
            Account = Acc.objects.get(id = Account_no)
            Balance = Account.balance
            data['name'] = Account.user_name.first_name
            data['Amount'] = Balance

            if request.method == "POST" :

                Beni_acc_no = int(request.POST["Beneficiary"])
                Beni_acc_no = int(Beni_acc_no) -1201100

                try:
                    Beni_account = Acc.objects.get(id = Beni_acc_no)

                except:
                    Beni_account = None

                if Beni_account :

                    transfer = int(request.POST['transfer'])

                    if transfer > 0 :

                        if Account.user_name != Beni_account.user_name:

                            if Balance >= transfer :

                                Account.balance = Account.balance - transfer

                                if Account.balance >= 0 :

                                    Result = statement(request,Account,Balance,-transfer,f"To{Beni_acc_no}")

                                    Account.save()

                                    Balance = Account.balance

                                    Newbalance = Beni_account.balance + transfer
                                    Result = statement(request,Beni_account,Newbalance,transfer,f"From{id}")
                                    Beni_account.balance = Newbalance
                                    Beni_account.save()

                                    data["Amount"] = Balance
                                    data['transfer'] = "Transition Successfull!!!!!"

                                    return render(request,"login/user.html",data)
                                
                                else : 
                                    data["Amount"] = Balance
                                    data['transfer'] = "Your Balance Is Zero 0"
                                    return render(request,"login/user.html",data)
                            
                            else : 

                                data['transfer'] = "Inefficient Balance"
                                return render(request,"login/user.html",data)
                            
                        elif Account.user_name == Beni_account.user_name:

                            Result = statement(request,Account,Balance,transfer,"Deposit")

                            Account.balance = Account.balance + transfer
                            Account.save()
                            Balance = Account.balance
                            
                            data["Amount"] = Balance
                            data['transfer'] = "Deposited Successfull!!!!!"

                            return render(request,"login/user.html",data)
                                              
                    else: 

                        data['transfer'] = "Enter 1 or more "
                        return render(request,"login/user.html",data)
                    
                else : 
                    data['transfer'] = "Beneficiary Does Not Exist !!!!"
                    return render(request,"login/user.html",data)

    except :
            data['tranfer'] = "Error"
            return render(request,"login/user.html",data)
    
    return render(request,"login/user.html",data)



#To Track Your Transition Through Login Account
def statement(request,acc_no,Balance,cash,details):

    try:

        statement = state(acc_no = acc_no, before_balance = Balance, cash_flow = cash, detail = details )
        statement.save()
        return True
    
    except:
        return False

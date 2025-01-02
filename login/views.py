from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Account as Acc, statement as state, User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

#To Login In Existing Account
def Login(request):

    #To Give Addition Info     
    
    '''
    To Login In Existing Account
    
    If request.method is POST it will cheak the form submition and try to authenticate the user
    If user is authenticated then it will login the user and redirect to account_detail page
    If user is not authenticated then it will return the same page with error message
    '''
    
    data = {"link":None,"url":"","pin":None}

    #TO Check Form Submition 
    if request.method == "POST":

        #Get Information From Form
        Account_no = str(request.POST["Account_no"])
        Passwrd = request.POST["password"]
        try:
            user = authenticate(request, username=Account_no, password=Passwrd)

            if user is not None:

                login(request, user)

                #Getting Account Detail According To Account No Given IN Form
                return HttpResponseRedirect(reverse("LoginApp:account"))
             
            else: 
                data["pass"] = "InValid Username Or PassWord!!!"
                return render(request,"login/Login.html", data)
            
        except :
            data["pass"] = "This Account Does Not Exist!!!"
            return render(request,"login/Login.html", data)

    return render(request,"login/Login.html", data)



#To LogOut 
def logout_view(request):
    """
    Logout the user and redirect to homepage
    """
    logout(request)
    return HttpResponseRedirect(reverse("Home"))



#To Display Account Detail After Login 
def account_detail(request):

    """Return account detail page with name, logout link, and account info."""
 
    print("account")
    account = Acc.objects.get(user_name = request.user)
    print(account.user_name)
    data = {
        "link": reverse("LoginApp:logout"),
        "url": "Logout",
        "pin": account.pin,
    }

    if account:
        data["detail"] = account
        return render(request, "login/account.html", data)

    return render(request, "login/account.html")



#To Deposit Money In Self Account Or Transfer Money To Other's Account
def moneyTransfer(request):
   
    """
    This view is used to deposit money in self account or transfer money to other's account.
    """
    data = {"link":reverse("LoginApp:logout"),"url":"Logout","pin":""}
    Account_no = request.user

    try:
            Account = Acc.objects.get(user_name = Account_no)
            Balance = Account.balance
            print(Account)
            print(Balance,'Bala')
            data["Amount"] = Balance
            data["pin"] = Account.pin

            if request.method == "POST" :

                if not Account.pin:
                    data["transfer"] = "Set your InCol pin first!!!"
                    return render(request,"login/user.html",data)
                print("!1")

                Beni_acc_no = int(request.POST["Beneficiary"])
                Beni_acc_no = int(Beni_acc_no) -1201100

                try:
                    Beni_account = Acc.objects.get(id = Beni_acc_no)
                    print("beni",Beni_account)

                except:
                    Beni_account = None

                if Beni_account :
                    print("H", Account.user_name == Beni_account.user_name)

                    transfer = int(request.POST['transfer'])

                    if transfer > 0 :

                        if Account.user_name != Beni_account.user_name:
                            print('1')
                                
                            if Balance >= transfer :
                                print("2")

                                Account.balance = Account.balance - transfer

                                if Account.balance >= 0 :
                                    print("3")
                                    request.session["Beni_acc_no"] = Beni_acc_no
                                    request.session["transfer"] = transfer

                                    return HttpResponseRedirect(reverse("LoginApp:pin"))
                                
                            else : 

                                data["transfers"] = "Inefficient Balance"
                                return render(request,"login/user.html",data)
                            
                        elif Account.user_name == Beni_account.user_name:

                            Balance = Account.balance + transfer
                            Result = statement(Account,Balance,transfer,"Deposit")
                            Account.balance = Balance
                            Account.save()
                            Balance = Account.balance
                            
                            data["Amount"] = Balance
                            data["transfers"] = "Deposited Successfull!!!!!"

                            return render(request,"login/user.html",data)
                                              
                    else: 

                        data["transfers"] = "Enter 1 or more "
                        return render(request,"login/user.html",data)
                    
                else : 
                    print("hello")
                    data["transfers"] = "Beneficiary Does Not Exist !!!!"
                    return render(request,"login/user.html",data)

    except :
            data["tranfers"] = "Error"
            return render(request,"login/user.html",data)
    
    return render(request,"login/user.html",data)


#To Track Your Transition Done By An Account Corresponding To The Current User 
def statement(acc_nos,Balance,cash,details):

    try:
        print("statement")
        print("!1",acc_nos)
        print("!2",Balance)
        print("!3",cash)
        print("!4",details)
        statement = state(acc_no = acc_nos, After_balance = Balance, cash_flow = cash, detail = details )
        statement.save()
        return True
    
    except:
        return False



#To Display The Statement Of An Account Corresponding To The Current User 
def view_statement(request,t=False):

    
    print(request.user)
    acc_no = Acc.objects.get(user_name = request.user)
    print(acc_no,"12")
    data = {"link":reverse("LoginApp:logout"),"url":"Logout","pin":acc_no.pin}
    t = request.GET.get('t')
    print('t',t)

    if t == 'True':
        Account = state.objects.filter(acc_no = acc_no)
        print("Account",Account)

        data["statement"] = Account
        print(data['statement'])
        return render(request,"login/Statement.html",data)
    
    else:
        if request.method == "GET":
            Account = state.objects.filter(acc_no = acc_no).order_by('-id')[:5]
            print(Account,"Acc")
            statements = []
            for statement in Account:
                print('addd',statement)
                statements.append({
                    'acc_no': statement.acc_no.id,
                    'balance': statement.before_balance,
                    'cash': statement.cash_flow,
                    'detail':statement.detail
                })
            print("add",statements)
            return HttpResponse(JsonResponse(statements, safe=False))



#To Confirm The InCol Pin Before MoneyTransfer Or Before Transition
def confirm_pin(request):
        
    Account_no = request.user
    print(Account_no)
    Account = Acc.objects.get(user_name = Account_no)
    Balance = Account.balance
    data = {"link":reverse("LoginApp:logout"),"url":"Logout","pin":Account.pin,"Amount":Balance}
    
    if request.method == "POST":
        Account = Acc.objects.get(user_name = Account_no)
        print(Account.pin,type(Account.pin))
        
        if Account.pin:
            
            print("f")
            pin = int(request.POST['pin'])
            print("pin",Account.pin,type(pin),type(Account.pin))
            print(pin == (Account.pin))

            try:
                if pin == (Account.pin):
                            
                            Beni_acc_no = request.session.get("Beni_acc_no")
                            transfer = int(request.session.get("transfer"))
                            print("Beni",Beni_acc_no)
                            print("transfer",transfer,type(transfer))
                            Beni_account = Acc.objects.get(id = Beni_acc_no)
                            print("beniacc",Beni_account)

                            print("pin",pin)
                            Balance = Account.balance - transfer
                            Result = statement(Account,Balance,-transfer,f"To{int(Beni_acc_no)+1201100}")
                            print("Result",Result)

                            if Result:
                                    Account.balance = Balance                         
                                    Account.save()

                                    Newbalance = Beni_account.balance + transfer
                                    Result = statement(Beni_account,Newbalance,transfer,f"From{id}")
                                    Beni_account.balance = Newbalance
                                    Beni_account.save()
                                    data["Amount"] = Balance
                                    data["transfers"] = "Transition Successfull!!!!!"

                                    return render(request,"login/user.html",data)
                            else:
                                
                                data["transfers"] = "Transition Unsuccessfull???"

                                return render(request,"login/user.html",data)
                else:
                    data["pass"] = "Fail"
                    return render(request, "login/pin.html", data)
            except:
                data["pass"] = "Error"
                return render(request, "login/pin.html", data)
            return render(request, "login/pin.html", data)

        elif not Account.pin:
            pin = request.POST['setpin']
            confirm_pin = request.POST['confirmpin']

            try:
                if pin == confirm_pin:
                    Account.pin = pin
                    Account.save()
                    data["pass"] = "Your InCol pin is Set"
                    return render(request, "login/pin.html", data)
                
                else:
                    data["pass"] = "Please Enter Same pin"
                    return render(request, "login/pin.html", data)  

            except:
                data["pass"] = "Errrr"
                return render(request, "login/pin.html", data)

    return render(request, "login/pin.html", data)
   
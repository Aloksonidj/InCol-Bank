from django.http import HttpResponseRedirect
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
                data['pass'] = "InValid Username Or PassWord!!!"
                return render(request,"login/Login.html", data)
            
        except :
            data['pass'] = "This Account Does Not Exist!!!"
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
def account_detail(request, account_id):
    """Return account detail page with name, logout link, and account info."""

    account = Acc.objects.get(id=account_id)
    data = {
        "name": account.user_name,
        "link": reverse("LoginApp:logout"),
        "url": "Logout",
        "pin": account.pin,
    }

    if account:
        data["detail"] = account
        return render(request, "login/account.html", data)

    return render(request, "login/account.html")



#To Deposit Money In Self Account Or Transfer Money To Other's Account
def moneyTransfer(request,id,pin=False):
    '''id: model.object(User) | pin (default = False)\n
    return render(user.html) with name: user.first_name | link: logout | url: "Logout | pin: urlto(pin.html)"'''

    data = {"name":"","link":reverse("LoginApp:logout"),"url":"Logout","pin":''}
    Account_no = int(id)-1201100
    print("id",id)

    try:
            Account = Acc.objects.get(id = Account_no)
            Balance = Account.balance
            data['name'] = Account.user_name.first_name
            data['Amount'] = Balance
            data["pin"] = Account.pin

            if request.method == "POST" :

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
                                
                            if not pin:
                                if Balance >= transfer :

                                    Account.balance = Account.balance - transfer

                                    if Account.balance >= 0 :

                                        return HttpResponseRedirect(reverse("LoginApp:pin", args=(id,)))
                                
                                else : 

                                    data['transfer'] = "Inefficient Balance"
                                    return render(request,"login/user.html",data)
                                
                            elif pin:
                                Result = statement(request,Account,Balance,-transfer,f"To{int(Beni_acc_no)+1201100}")

                                if Result:

                                    Account.save()

                                    Balance = Account.balance

                                    Newbalance = Beni_account.balance + transfer
                                    Result = statement(request,Beni_account,Newbalance,transfer,f"From{int(id)+1201100}")
                                    Beni_account.balance = Newbalance
                                    Beni_account.save()

                                    data["Amount"] = Balance
                                    data['transfer'] = "Transition Successfull!!!!!"

                                    return render(request,"login/user.html",data)
                                else:
                                    data['transfer'] = "Transition Unsuccessfull???"

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
                    print("hello")
                    data['transfer'] = "Beneficiary Does Not Exist !!!!"
                    return render(request,"login/user.html",data)

    except :
            data['tranfer'] = "Error"
            return render(request,"login/user.html",data)
    
    return render(request,"login/user.html",data)



#To Track Your Transition Done By An Account Corresponding To The Current User 
def statement(request,acc_no,Balance,cash,details):
    '''request | acc_no: model.object(Account) | Balance: Integer | cash: Integer | details: string(from/to cash come/go)'''

    try:

        statement = state(acc_no = acc_no, before_balance = Balance, cash_flow = cash, detail = details )
        statement.save()
        return True
    
    except:
        return False



#To Display The Statement Of An Account Corresponding To The Current User 
def view_statement(request,account_no):
    '''account_no: model.object(User) -> String'''
    print("account_no",type(account_no))
    
    user = User.objects.get(username = account_no)
    account_no = int(account_no) - 1201100
    acc_no = Acc.objects.get(user_name = user)
    data = {"name":acc_no.user_name,"link":reverse("LoginApp:logout"),"url":"Logout","pin":acc_no.pin}

    Account = state.objects.filter(acc_no = acc_no)
    data["statement"] = Account
    return render(request,"login/Statement.html",data)



#To Confirm The InCol Pin Before MoneyTransfer Or Before Transition
def confirm_pin(request,id):
        
    Account_no = int(id)-1201100
    t = request.GET.get('t')
    print(t)
    Account = Acc.objects.get(id = Account_no)
    data = {"name":Account.user_name,"link":reverse("LoginApp:logout"),"url":"Logout","pin":Account.pin}
    
    if request.method == "POST":
        
        if t == True:
            pin = request.POST['pin']
            print("pin",Account.pin)

            try:
                if pin == Account.pin:
                    moneyTransfer(id,pin=True)
                else:
                    data['pass'] = "Fail"
                    return render(request, "login/pin.html", data)
            except:
                data['pass'] = "Error"
                return render(request, "login/pin.html", data)
            return render(request, "login/pin.html", data)
        
    return render(request, "login/pin.html", data)
   
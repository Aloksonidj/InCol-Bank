from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Account as Acc, statement as state, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
                messages.success(request, "Login Successfull!!!")
                return HttpResponseRedirect(reverse("LoginApp:account"))
             
            else: 
                messages.error(request,"InValid Username Or PassWord!!!")
                return render(request,"login/Login.html", data)
            
        except :
            messages.error(request,"InValid Username Or PassWord!!!")
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

    print("account_detail")
    print("account")
    account = Acc.objects.get(user_name = request.user)
    print(account.user_name)
    data = {
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
    
    :param request: request object
    :return: render login/transfer.html with data
    """
    print("moneyTransfer")
    
    data = {
        "link":reverse("LoginApp:logout"),
        "url":"Logout",
        "pin":"",
        "transfers":"",
        }
    Account_no = request.user

    try:
            # Get the account detail
            Account = Acc.objects.get(user_name = Account_no)
            Balance = Account.balance
            print(Account)
            print(Balance,'Bala')
            data["Amount"] = Balance
            data["pin"] = Account.pin

            if request.method == "POST":
                print("post")

                # Check if the account has set the InCol pin
                if not Account.pin:
                    data["transfers"] = "Set your InCol pin first!!!"
                    data['t'] = reverse("LoginApp:pin")
                    return render(request,"login/transfer.html",data)
                print("!1")

                # Get the beneficiary account information
                Beni_acc_no = int(request.POST["Beneficiary"])
                Beni_acc_no = int(Beni_acc_no) -1201100

                try:
                    Beni_account = Acc.objects.get(id = Beni_acc_no)
                    print("beni",Beni_account)

                except:
                    Beni_account = None

                if Beni_account :
                    print("H", Account.user_name == Beni_account.user_name)

                    # Get the amount to transfer
                    transfer = int(request.POST['transfer'])

                    # Check if the amount is valid
                    if transfer > 0 :

                        # Check if the account is not the same as the beneficiary account
                        if Account.user_name != Beni_account.user_name:
                            print('1')
                                
                            # Check if the account has sufficient balance
                            if Balance >= transfer :
                                print("2")

                                # Decrease the balance
                                Account.balance = Account.balance - transfer

                                # Check if the balance is not negative
                                if Account.balance >= 0 :
                                    print("3")
                                    request.session["Beni_acc_no"] = Beni_acc_no
                                    request.session["transfer"] = transfer

                                    # Redirect to the confirm pin page
                                    return HttpResponseRedirect(reverse("LoginApp:pin"))
                                
                            else : 

                                # Set the error message
                                data["transfers"] = "Inefficient Balance"
                                return render(request,"login/transfer.html",data)
                            
                        elif Account.user_name == Beni_account.user_name:

                            # Deposit the money in the account
                            Balance = Account.balance + transfer
                            Result = statement(Account,Balance,transfer,"Deposit")
                            Account.balance = Balance
                            Account.save()
                            Balance = Account.balance
                            
                            # Set the success message
                            data["Amount"] = Balance
                            data["transfers"] = "Deposited Successfull!!!!!"


                            return render(request,"login/transfer.html",data)
                                              
                    else: 

                        # Set the error message
                        data["transfers"] = "Enter 1 or more "
                        return render(request,"login/transfer.html",data)
                    
                else : 
                    # Set the error message
                    data["transfers"] = "Beneficiary Does Not Exist !!!!"
                    return render(request,"login/transfer.html",data)

    except Exception as e:
            # Set the error message
            print(e)
            data["tranfers"] = e
            return render(request,"login/transfer.html",data)
    
    return render(request,"login/transfer.html",data)



#To Track Your Transition Done By An Account Corresponding To The Current User 
def statement(acc_nos, Balance, cash, details):
    """
    This function creates a new statement in the database 
    corresponding to the account number, balance, cash flow and details
    
    Parameters:
    acc_nos (Acc): The account number corresponding to the statement
    Balance (int): The balance of the account at the time of transaction
    cash (int): The amount of money in the transaction
    details (str): The details of the transaction
    
    Returns:
    bool: True if the statement is created successfully else False
    """
    print("statement")
    try:
        print("statement")
        statement = state(acc_no=acc_nos, After_balance=Balance, cash_flow=cash, detail=details)
        statement.save()
        return True
    
    except:
        return False



#To Display The Statement Of An Account Corresponding To The Current User 
def view_statement(request,t=False):
    """
    View statement of the current user
    if t is True then render the statement in Statement.html
    else return the statement in json format
    Parameters:
    request (HttpRequest): The request object
    t (bool): If True then render the statement in Statement.html
    """
    print("view_statement")
    print(request.user)
    acc_no = Acc.objects.get(user_name = request.user)
    print(acc_no,"12")
    data = {"link":reverse("LoginApp:logout"),"url":"Logout","pin":acc_no.pin}
    t = request.GET.get('t')
    print('t',t)

    if t == 'True':
        # Get the statement of the current user
        Account = state.objects.filter(acc_no = acc_no).order_by('-id')
        print("Account",Account)

        # Add the statement to the data
        data["statement"] = Account
        print(data['statement'])
        # Render the statement in Statement.html
        return render(request,"login/Statement.html",data)
    
    else:
        if request.method == "GET":
            # Get the statement of the current user 
            # order by the id in descending order and get the first 5
            Account = state.objects.filter(acc_no = acc_no).order_by('-id')[:5]
            print(Account,"Acc")
            statements = []
            for statement in Account:
                
                # Add the statement to the list
                statements.append({
                    'acc_no': statement.acc_no.id,
                    'balance': statement.After_balance,
                    'cash': statement.cash_flow,
                    'detail':statement.detail
                })
            # Return the statement in json format
            return HttpResponse(JsonResponse(statements, safe=False))



#To Confirm The InCol Pin Before MoneyTransfer Or Before Transition
def confirm_pin(request):
    """
    Confirm the InCol pin before money transfer or before transition
    Parameters:
    request (HttpRequest): The request object
    """
    print("Confirm pin")
        
    Account_no = request.user
    print(Account_no)
    Account = Acc.objects.get(user_name = Account_no)
    Balance = Account.balance
    data = {
        "link":reverse("LoginApp:logout"),
        "url":"Logout",
        "pin":Account.pin,
        "Amount":Balance
    }
    
    if request.method == "POST":
        Account = Acc.objects.get(user_name = Account_no)
        print(Account.pin,type(Account.pin))
        
        if Account.pin:
            # If the InCol pin is already set
            pin = int(request.POST['pin'])
            print("pin",Account.pin,type(pin),type(Account.pin))
            print(pin == (Account.pin))

            try:
                if pin == (Account.pin):
                            # If the pin is correct
                            # Get the beneficiary account number and the amount
                            # to transfer from the session
                            Beni_acc_no = request.session.get("Beni_acc_no")
                            transfer = int(request.session.get("transfer"))
                            
                            Beni_account = Acc.objects.get(id = Beni_acc_no)

                            Balance = Account.balance - transfer

                            try:
                                    # Create a new statement for the current user
                                    Result = statement(Account,Balance,-transfer,f"To {int(Beni_acc_no)+1201100}")
                                    print("Result",Result)

                                    # Update the balance of the current user
                                    Account.balance = Balance                         
                                    Account.save()

                                    # Create a new statement for the beneficiary
                                    Newbalance = Beni_account.balance + transfer
                                    Result = statement(Beni_account,Newbalance,transfer,f"From {Account.user_name}")
                                    # Update the balance of the beneficiary
                                    Beni_account.balance = Newbalance
                                    Beni_account.save()
                                    # Update the data
                                    data["Amount"] = Balance
                                    messages.success(request, "Transition Successfull!!!!!")

                                    return redirect(reverse("transfer"))
                            except:
                                # If there is any error
                                data["transfers"] = "Transition Unsuccessfull???"

                                return render(request,"login/transfer.html",data)
                else:
                    # If the pin is incorrect
                    data["pass"] = "Fail"

                    return render(request, "login/pin.html", data)
            except:
                # If there is any error
                data["pass"] = "Error"

                return render(request, "login/pin.html", data)
            
            return render(request, "login/pin.html", data)

        elif not Account.pin:
            # If the InCol pin is not set
            pin = request.POST['setpin']
            confirm_pin = request.POST['confirmpin']

            try:
                if pin == confirm_pin:
                    # If the pin is correct
                    Account.pin = pin
                    Account.save()
                    # Update the data
                    data["pass"] = "Your InCol pin is Set"
                    return render(request, "login/pin.html", data)
                
                else:
                    # If the pin is incorrect
                    data["pass"] = "Please Enter Same pin"
                    return render(request, "login/pin.html", data)  

            except:
                # If there is any error
                data["pass"] = "Errrr"
                return render(request, "login/pin.html", data)

    return render(request, "login/pin.html", data)
   
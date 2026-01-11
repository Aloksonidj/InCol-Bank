from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Account as Acc, statement as state, User
from django.contrib.auth import authenticate, login, logout, decorators
from django.contrib import messages

# Create your views here.

# helper functions
def confirm_pin(request,pin):
    print("confirm_pin")
    '''
    Confirm if the pin matches the user's InCol pin
    
    Parameters:
        request (HttpRequest): The request object
        pin (int): The pin to be confirmed
        t (bool): If True, the function will return False if the user is not authenticated
            (default is False)
    
    Returns:
        bool: True if the pin matches, False otherwise
    '''
    try:
        Account = Acc.objects.get(user_name = request.user)
        if Account.pin == pin:
            return True
    except Exception as e:
        print("Error:", e)
        return False
    return False


#To Login In Existing Account
def Login(request):
    print("Login")
    '''
    To Login In Existing Account
    
    If request.method is POST it will cheak the form submition and try to authenticate the user
    If user is authenticated then it will login the user and redirect to account_detail page
    If user is not authenticated then it will return the same page with error message
    '''    
    data = {"pin":None}

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
@decorators.login_required
def logout_view(request):
    """
    Logout the user and redirect to homepage
    """
    logout(request)
    return HttpResponseRedirect(reverse("Home"))


#---------------------------------Routes functions--------------------------------------------------------------------------
#To Display Account Detail After Login 
@decorators.login_required
def account_detail(request):

    """Return account detail page with name, logout link, and account info."""

    print("account_detail")
    account = Acc.objects.get(user_name = request.user)
    data = {
        "pin": account.pin,
    }

    if account:
        data["detail"] = account
        return render(request, "login/account.html", data)

    return render(request, "login/account.html")


@decorators.login_required
def checkBalance(request):
    print("checkBalance")
    '''
    Set the action type to 'check_balance' and redirect to the pin page

    This function is used to check the balance of the user's account. It sets the
    "action_type" key in the request session to "check_balance". This key is used
    by the pin view to determine whether to show the balance of the account
    after the user has entered their InCol pin.

    After setting the key, this function redirects to the pin page.

    :param request: request object
    :return: HttpResponseRedirect to the pin page
    '''
    request.session['action_type'] = 'check_balance' 
    return HttpResponseRedirect(reverse("LoginApp:pin"))


@decorators.login_required
def hide_balance(request):
    print("hide_balance")
    '''
    Hides the balance of the user's account
    
    This function removes the "show_balance" key from the request session if it exists.
    If the key is removed, it prints "show_balance deleted".
    Then, it redirects back to the account page.
    '''
    if "show_balance" in request.session:
        del request.session["show_balance"]
        print("show_balance deleted")
    
    # If this was called via a direct link, redirect back to the account page
    return redirect(reverse("LoginApp:account"))


#To Deposit Money In Self Account Or Transfer Money To Other's Account
@decorators.login_required
def moneyTransfer(request):
    """
    This view is used to deposit money in self account or transfer money to other's account.
    
    :param request: request object
    :return: render login/transfer.html with data
    """
    print("moneyTransfer")
    
    data = {
        "pin":"",
        }
    Account_no = request.user

    try:
        # Get the account detail
        Account = Acc.objects.get(user_name = Account_no)
        Balance = Account.balance
        data["Amount"] = Balance
        data["pin"] = Account.pin

        if request.method == "POST":

            # Check if the account has set the InCol pin
            if not Account.pin:
                messages.warning(request,"Set your InCol pin first!!!")
                return redirect("LoginApp:pin")

            # Get the beneficiary account information
            Beni_acc_no = int(request.POST["Beneficiary"])
            Beni_acc_no = int(Beni_acc_no) - 1201100

            try:
                Beni_account = Acc.objects.get(id = Beni_acc_no)

            except:
                Beni_account = None

            if Beni_account :

                # Get the amount to transfer
                transfer = int(request.POST['transfer'])

                # Check if the amount is valid
                if transfer > 0 :

                    # Check if the account is not the same as the beneficiary account
                    if Account.user_name != Beni_account.user_name:
                    
                    # Check if the account has sufficient balance
                        if Balance >= transfer and Account.balance >= 0 :

                            # Decrease the balance
                            Account.balance = Account.balance - transfer

                            request.session["Beni_acc_no"] = Beni_acc_no
                            request.session["transfer"] = transfer

                            # Redirect to the confirm pin page
                            return HttpResponseRedirect(reverse("LoginApp:pin"))
                            
                        else : 
                            # Set the error message
                            messages.warning(request,"Insufficient Balance!!!")
                            return render(request,"login/transfer.html",data)
                    
                    elif Account.user_name == Beni_account.user_name:

                        # deposit the money in the account
                        Balance = Account.balance + transfer
                        Result = statement(Account,Balance,transfer,"Deposit")
                        Account.balance = Balance
                        Account.save()
                        Result.save()
                        Balance = Account.balance
                        
                        # Set the success message
                        data["Amount"] = Balance
                        messages.success(request,"Money Deposited Successfully!!!")
                        return render(request,"login/transfer.html",data)
                                              
                else: 

                    # Set the error message
                    messages.warning(request,"Enter 1 or more amount.")
                    return render(request,"login/transfer.html",data)
            
            else : 
                # Set the error message
                messages.error(request,"Beneficiary Does Not Exist !!!!")
                return render(request,"login/transfer.html",data)

    except Exception as e:
        # Set the error message
        print(e)
        messages.debug(request,f"Error{e}")
        return render(request,"login/transfer.html",data)
    
    return render(request,"login/transfer.html",data)


#To Confirm The InCol Pin Before MoneyTransfer Or Before Transition
@decorators.login_required
def confirm_pay(request):
    """
    Confirm the InCol pin before money transfer or before transition
    Parameters:
    request (HttpRequest): The request object
    """
    print("confirm_pay")
        
    Account_no = request.user
    Account = Acc.objects.get(user_name = Account_no)
    data = {
        "pin":Account.pin,
    }
    
    if request.method == "POST":
        Account = Acc.objects.get(user_name = Account_no)
        
        if Account.pin:
            # If the InCol pin is already set
            pin = int(request.POST['pin'])

            try:
                is_valid = confirm_pin(request,pin)
                
                if is_valid :
                    # If the pin is correct

                    action = request.session.get('action_type')
                    
                    if action == 'check_balance':
                        request.session['show_balance'] = True 
                        del request.session['action_type']
                        return HttpResponseRedirect(reverse("LoginApp:account"))
                    

                    # Get the beneficiary account number and the amount
                    # to transfer from the session
                    Beni_acc_no = request.session.get("Beni_acc_no")
                    transfer = int(request.session.get("transfer"))
                    
                    Beni_account = Acc.objects.get(id = Beni_acc_no)
                    
                    Balance = Account.balance - transfer

                    try:
                        # Create a new statement for the current user
                        Result1 = statement(Account,Balance,-transfer,f"to {int(Beni_acc_no)+1201100}")

                        # Update the balance of the current user
                        Account.balance = Balance                      

                        # Create a new statement for the beneficiary
                        Newbalance = Beni_account.balance + transfer
                        Result2 = statement(Beni_account,Newbalance,transfer,f"From {Account.user_name}")
                        
                        # Update the balance of the beneficiary
                        Beni_account.balance = Newbalance
                        if Result1 and Result2:
                            Account.save()
                            Beni_account.save()
                            # Update the data
                            messages.success(request, "Transition Successfull!!!!!")

                            return HttpResponseRedirect(reverse("LoginApp:transfer"))
                    except Exception as e:
                        # If there is any error
                        print(e)
                        messages.error(request, "Transition Unsuccessfull???")

                        return render(request,"login/transfer.html",data)
                        
                        
                else:
                    # If the pin is incorrect
                    messages.error(request, "Incorrect Pin")

                    return render(request, "login/pin.html", data)
            except Exception as e:
                # If there is any error
                print(e)
                messages.debug(request, f"Error{e}")

                return render(request, "login/pin.html", data)
            
            return render(request, "login/pin.html", data)

        elif not Account.pin:
            # If the InCol pin is not set
            pin = request.POST['setpin']
            pin_confirm = request.POST['confirmpin']

            try:
                if pin == pin_confirm:
                    # If the pin is correct
                    Account.pin = pin
                    Account.save()
                    # Update the data
                    messages.success(request, "Pin Set Successfull!!!")
                    return redirect("LoginApp:account")
                
                else:
                    # If the pin is incorrect
                    messages.error(request, "Pin Not Matched")
                    return render(request, "login/pin.html", data)  

            except Exception as e:
                # If there is any error
                print(e)
                messages.debug(request, f"Error{e}")
                return render(request, "login/pin.html", data)

    return render(request, "login/pin.html", data)
 

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
    print("statement function started")
    try:
        statement = state(acc_no=acc_nos, After_balance=Balance, cash_flow=cash, detail=details)
        statement.save()
        return True
    
    except Exception as e:
        print(f"statement function: error {e}")
        return False


#To Display The Statement Of An Account Corresponding To The Current User 
@decorators.login_required
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
    acc_no = Acc.objects.get(user_name = request.user)
    data = {"link":reverse("LoginApp:logout"),"url":"Logout","pin":acc_no.pin}
    t = request.GET.get('t')

    if t == 'True':
        # Get the statement of the current user
        Account = state.objects.filter(acc_no = acc_no).order_by('-id')

        # Add the statement to the data
        data["statement"] = Account
        # Render the statement in Statement.html
        return render(request,"login/Statement.html",data)
    
    else:
        if request.method == "GET":
            # Get the statement of the current user 
            # order by the id in descending order and get the first 5
            Account = state.objects.filter(acc_no = acc_no).order_by('-id')[:5]
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
        
        
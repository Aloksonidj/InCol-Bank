from django.http import HttpResponseRedirect
from login.models import Account , User, statement
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db import IntegrityError


def Home(request):
    """
    To Render The Home Page
    This is the main page of the Bank which will show two options
    1. To Open a new Account
    2. To Login into an existing Account
    """
    return render(request,"Bank.html")


def newAccount(request):
    """
    To Create a new Account in the Bank
    This function will create a new user and account in the database
    and then login the user and redirect them to the account detail page
    """
    data = {
        "pass": None,
        "Account": '',
        "Acc_no": '',
        "name": None,
        "link": None,
        "url": None,
        "pin": None
    }

    try:
        if request.method == "POST":
            # Get the information from the form
            name = request.POST["User"]
            password = request.POST["password"]
            confirm_password = request.POST['confirm_password']
            Mobile = request.POST["Mobile_no"]

            # Check if the password and confirm password is the same
            if password == confirm_password:
                # Create a new user in the database
                try:
                    user = User.objects.create_user(username=name, password=password)
                    user.save()
                except IntegrityError:
                    # If the username is already taken then return the same page with an error message
                    data = {
                        "pass": None,
                        "Account": "Username already taken.",
                        "Acc_no": '',
                        "name": '',
                        "pin": None
                    }
                    return render(request, "open_Acc.html", data)

                # Create a new account in the database
                record = Account(user_name=user, Mobile_no=Mobile)
                record.save()

                # Update the user's username to be the account number
                user.first_name = user.username
                user.username = f'{1201100+record.id}'
                user.save()

                # Create a new statement for the account
                Balance = 2000
                transfer = 2000
                Result = statement(user, Balance, transfer, "Deposit")
                Result.save()

                # Login the user and redirect them to the account detail page
                login(request, user)
                return HttpResponseRedirect(reverse('LoginApp:account'))
            
            else:
                # If the password and confirm password is not the same then return the same page with an error message
                data = {
                    "pass": "Password and confirm password is not the same",
                    "Account": '',
                    "Acc_no": '',
                    "name": '',
                    "pin": None
                }
                return render(request, "open_Acc.html", data)

    except:
        # If there is any error then return the same page with an error message
        data["Acc_no"] = "Something Wrong !!!"
        return render(request, "open_Acc.html", data)


    return render(request, "open_Acc.html", data)


def check_user(request):
    print("check_user")
    if request.method == "POST":
        if request.user.is_authenticated:
            pwrd = request.POST.get("pwrd")

            try:
                account = Account.objects.get(user_name=request.user)
                if account and request.user.check_password(pwrd):
                    request.session["account_details"] = {
                        "user":request.user.username,
                        "is_verfied":True
                    }
                    return HttpResponseRedirect(reverse("changepass"))
                
            except Exception as e:
                print("Error:", e)
                messages.debug(request, "Error in checking user.")
        
        else:
            username = request.POST.get("acc_no")
            mobile = request.POST.get('mobile')

            try:
                user = User.objects.get(username=username)
                account = Account.objects.get(user_name=user, Mobile_no=mobile)
                if account:
                    request.session["account_details"] = {
                        "user":username,
                        "is_verfied":True
                    }
                    return HttpResponseRedirect(reverse("changepass"))
                
            except User.DoesNotExist:
                print("User does not exist")
                messages.error(request, "Invalid Account Number or Mobile Number.")

    return render(request,"check_user.html")


def change_password(request):
    print("change_password")
    if request.method == "POST":
        new_pw = request.POST.get("new_password")
        confirm_pw = request.POST.get("confirm_password")

        try:
            account = request.session.get("account_details")
            
            if account['is_verfied']:
                user = User.objects.get(username=account['user'])

                if new_pw == confirm_pw:
                    user.set_password(new_pw) 
                    user.save()
                    messages.success(request, "Password updated successfully! Please login.")
                    del request.session['account_details']
                    if request.user.is_authenticated:
                        return redirect(reverse("LoginApp:account"))
                    return redirect(reverse("LoginApp:login"))
                else:
                    messages.error(request, "Passwords do not match.")  
        
        except (User.DoesNotExist, Account.DoesNotExist):
            messages.error(request, "Invalid Account Number or Mobile Number.")

    return render(request, "forget_password.html")


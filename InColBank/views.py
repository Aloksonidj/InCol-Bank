from django.http import HttpResponseRedirect
from login.models import Account , User, statement
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login
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


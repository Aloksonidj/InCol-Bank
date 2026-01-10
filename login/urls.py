from django.urls import include,path
from login import views

app_name= "LoginApp"

urlpatterns = [

    path("", views.Login, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("account/",views.account_detail, name="account"),
    path("transfer/",views.moneyTransfer, name="transfer"),
    path("account/statement/", views.view_statement, name="statement"),
    path("transfer/pin",views.confirm_pay, name="pin"),
    path("account/check-balance/", views.checkBalance, name="check_balance"),
    path("account/hide-balance/", views.hide_balance, name="hide_balance"),

]

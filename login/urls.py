from django.urls import include,path
from login import views

app_name= "LoginApp"

urlpatterns = [

    path("", views.Login, name="login"),
    path('logout', views.logout_view, name="logout"),
    path("<int:acc>",views.accountDetail, name='account'),
    path("transfer/<int:id>",views.moneyTransfer, name='transfer'),

]

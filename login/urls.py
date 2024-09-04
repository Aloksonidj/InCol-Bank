from django.urls import include,path
from login import views

app_name= "LoginApp"

urlpatterns = [
    path("", views.Login, name="login")
]

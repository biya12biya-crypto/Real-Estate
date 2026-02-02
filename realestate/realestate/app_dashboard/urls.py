from django.urls import path

from app_dashboard import views


app_name="dashboard"
urlpatterns = [
    path("admin/",views.admin),
    path("",views.guest),
    path("login/",views.log,name="login"),
  path("sellerreg/",views.sellerreg,name='sellerreg'),
  path("buyerreg/",views.buyerreg,name='buyerreg'),
    path("sellerdashboard/",views.sellerdashboard,name='sellerdashboard'),
    path("buyerdashboard/",views.buyerdashboard,name='buyerdashboard'),
    path("logout/",views.logout_view,name='logout'),

    


]
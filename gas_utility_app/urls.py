from django.urls import path
from . import views
from .views import user_logout

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('', views.customer_signup, name='customer_signup'),
   # path('customer/signup/', views.customer_signup, name='customer_signup'),
    path('staff/signup/', views.staff_member_signup, name='staff_member_signup'),
    path('customer/service_request_form/', views.Customer_home, name='service_request_form'),
    path('staff/support_request_list/',views.Staff_home,name='support_request_list'),

    path('submit-service-request/', views.service_request_submit, name='submit_service_request'),

    path('account-information/', views.account_info, name='account_information'),
    path('logout/', user_logout, name='logout'),
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name='search'
urlpatterns = [
    path('', views.SearchListView.as_view(), name='all'),
    path('search/<int:pk>', views.SearchDetailView.as_view(), name='search_detail'),
]
try:
    social_login = 'registration/login.html'
    urlpatterns.insert(0,
                       path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                       )
    print('Using', social_login, 'as the login template')
except:
    print('Using registration/login.html as the login template')

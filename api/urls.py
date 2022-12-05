from django.contrib import admin
from django.urls import path
from . views import *


urlpatterns = [
    path('', index_page, name='api-index-page'),
    path('account/create-user/', create_user_page, name='api-account-create-user-page'),
    path('account/get-user/', get_user_page, name='api-account-get-user-page')
]

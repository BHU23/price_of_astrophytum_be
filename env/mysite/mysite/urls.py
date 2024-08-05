"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/prices/', views.PriceListCreate.as_view(), name='price-list-create'),
    path('api/prices/<int:pk>/', views.PriceDetail.as_view(), name='price-detail'),
    path('api/classes/', views.ClassListCreate.as_view(), name='class-list-create'),
    path('api/classes/<int:pk>/', views.ClassDetail.as_view(), name='class-detail'),
    path('api/history-predictions/', views.HistoryPredictionsListCreate.as_view(), name='history-predictions-list-create'),
    path('api/history-predictions/<int:pk>/', views.HistoryPredictionsDetail.as_view(), name='history-predictions-detail'),
    path('api/predictions/', views.PredictionsListCreate.as_view(), name='predictions-list-create'),
    path('api/predictions/<int:pk>/', views.PredictionsDetail.as_view(), name='predictions-detail'),
]

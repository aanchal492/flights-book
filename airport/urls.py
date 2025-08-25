from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('book-flight/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('contact/', views.contact, name='contact'),
    
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('booking-summary/<int:flight_id>/', views.booking_summary, name='booking_summary'),
]

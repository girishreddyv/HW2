from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('movies/', views.list_movies, name='movies'),
    path('movies/<int:id>', views.movie_details, name='movie'),
    path('bookings/book', views.book_movie, name='booking'),
    path('bookings/history/<int:user_id>', views.user_movie_booking_history, name='history'),
]

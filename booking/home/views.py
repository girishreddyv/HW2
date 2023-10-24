from django.shortcuts import render,HttpResponse
import json
from datetime import datetime
from django.utils import timezone
from rest_framework import status
from home.models import Movie, Booking
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view

User =get_user_model()


@api_view(['GET'])
def home(request):
    return HttpResponse("welcome to movie protal")

@api_view(['GET'])
def list_movies(request):
    movies_list = Movie.objects.all()
    movies_serialized = [{'id': movie.id, 'title': movie.title} for movie in movies_list]
    context = {'movies_list': movies_serialized}
    return render(request, 'movies_list.html', context)


@api_view(['GET'])
def movie_details(request, id: int):
    try:
        movie = Movie.objects.get(id=id)
        movie_serialized = {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'showtimes': [showtime.time.strftime('%Y-%m-%d %H:%M:%S') for showtime in movie.showtime_set.all()]
        }
        context = {'movie_details': movie_serialized}
        return render(request, 'movie_details.html', context)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie with id not found'}, safe=False, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', 'POST'])
def book_movie(request):
    if request.method == 'POST':
        try:
            data = request.data  # Use request.data to access form data

            # Parse the string and create a datetime object
            parsed_datetime = datetime.strptime(data.get('showtime'), "%Y-%m-%d %H:%M:%S")
            showtime = timezone.make_aware(parsed_datetime, timezone.get_current_timezone())
            form_data = {'seat': data.get('seat'), 'showtime': showtime}
            booking = Booking.objects.create(**form_data)
            booking.user = User.objects.get(id=data.get('user'))
            booking.movie = Movie.objects.get(id=data.get('movie'))
            booking.save()

            # Render the booking confirmation HTML template or any other response
            return render(request, 'booking_confirmation.html')
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'message': 'Invalid data format'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': f'{e}'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
    else:
        # If it's a GET request, render the booking form
        return render(request, 'booking_form.html')




@api_view(['GET'])
def user_movie_booking_history(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        history = Booking.objects.filter(user=user)
        bookings = [{'movie': booking.movie.title, 'seat': booking.seat, 'time': booking.showtime.strftime('%Y-%m-%d %H:%M:%S')} for booking in history]
        context = {'bookings': bookings}
        return render(request, 'user_booking_history.html', context)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User with id not found'}, safe=False, status=status.HTTP_404_NOT_FOUND)

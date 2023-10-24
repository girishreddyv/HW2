from rest_framework import serializers
from home.models import Movie, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model =Movie
        fields ='__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model =Booking
        fields ='__all__'
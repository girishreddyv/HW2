from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from home.models import Movie, Booking
from datetime import datetime, timezone
from home.models import Movie
from home.serializers import MovieSerializer

User = get_user_model()

class IntegrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.movie = Movie.objects.create(title="Test Movie", description="Test description")

    def test_api_movie_list(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_api_movie_details(self):
        response = self.client.get(f'/movies/{self.movie.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.movie.title)

    def test_api_booking(self):
        data = {
            'user': self.user.id,
            'movie': self.movie.id,
            'seat': '10A',
            'showtime': '2023-10-10 12:30:10'
        }
        response = self.client.post('/bookings/book', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 1)

    def test_api_user_history(self):
        response = self.client.get(f'/bookings/history/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

class UnitTestCase(TestCase):
    def test_booking_seat_availability(self):
        parsed_datetime = datetime.strptime('2023-10-10 12:30:10', "%Y-%m-%d %H:%M:%S")
        tzi = timezone.make_aware(parsed_datetime, timezone.get_current_timezone())
        Booking.objects.create(seat="10A", showtime=tzi)
        available = Booking.is_seat_available(tzi, "10A")
        self.assertFalse(available)

    def test_user_booking_history(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        movie = Movie.objects.create(title="Test Movie", description="Test description")
        parsed_datetime = datetime.strptime('2023-10-10 12:30:10', "%Y-%m-%d %H:%M:%S")
        tzi = timezone.make_aware(parsed_datetime, timezone.get_current_timezone())
        Booking.objects.create(seat="10A", showtime=tzi, user=user, movie=movie)
        history = Booking.get_user_booking_history(user)
        self.assertEqual(len(history), 1)

    def test_serializer_json_transformation(self):
        movie = Movie.objects.create(title="Test Movie", description="Test description")
        serializer = MovieSerializer(movie)
        data = serializer.data
        expected_data = {'id': movie.id, 'title': "Test Movie", 'description': "Test description"}
        self.assertEqual(data, expected_data)



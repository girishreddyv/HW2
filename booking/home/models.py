from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null =False)
	
    def __str__(self):
        return self.title
    
class Showtime(models.Model):
    time =models.DateTimeField()
    movie =models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null =True)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE, null =True)
    seat = models.CharField(max_length =10)
    showtime =models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user.username} booked seat {self.seat}"

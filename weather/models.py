from django.db import models


class Temperature(models.Model):
    email = models.EmailField()
    place = models.CharField(max_length=255)
    temperature = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} - {self.temperature}°C - {self.created_at}'

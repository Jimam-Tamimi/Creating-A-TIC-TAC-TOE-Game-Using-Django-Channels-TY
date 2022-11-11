from django.db import models

# Create your models here.

class Room(models.Model):
    
    def __str__(self) -> str:
        return f"{self.id}"
from django.db import models

# Create your models here.
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

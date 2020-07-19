from django.db import models

class Lobby(models.Model):
    title = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title

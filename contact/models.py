from django.db import models

# Create your models here.
class VisitorMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    def __str__(self):
        return self.name

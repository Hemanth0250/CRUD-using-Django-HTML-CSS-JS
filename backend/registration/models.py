from django.db import models  # type: ignore

# Create your models here.
class Registration(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phoneno = models.BigIntegerField()
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name
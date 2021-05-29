from django.db import models

# Create your models here.
class Order(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    balhyo = models.CharField(max_length=100)
    hyang = models.CharField(max_length=100)
    num = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name
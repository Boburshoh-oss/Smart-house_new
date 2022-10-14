from django.db import models
from uuid import uuid4

# Create your models here.

class Home(models.Model):
    """
    Home model.
    """
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(to='account.User', on_delete=models.CASCADE,blank=True,null=True)
    key = models.CharField(max_length=200,blank=True,null=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Channel(models.Model):
    owner = models.ForeignKey(to='account.User', on_delete=models.CASCADE, blank=True,null=True)
    name = models.CharField(max_length=200) # lampa
    description = models.TextField(max_length=200,blank=True,null=True)
    device = models.ForeignKey('mysite.Device',on_delete=models.CASCADE,null=True,related_name="channels")
    topic_name = models.CharField(max_length=200,unique=True,blank=True,null=True)
    state = models.CharField(
        max_length=100,
        choices=[
            ("on", "ON"),
            ("off", "OFF"),
        ],
        default="off",
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        self.topic_name = f"{self.device.home}{self.device.home.key}/{self.device}/{self.name}"
        return super().save()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['device', 'name'], 
                name='unique channel'
            )
        ]

class Device(models.Model):
    owner = models.ForeignKey(to='account.User', on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    product = models.ForeignKey(
        "mysite.Product", on_delete=models.SET_NULL, related_name="devices", null=True
    )
    home = models.ForeignKey(
        "mysite.Home", on_delete=models.CASCADE, related_name="devices_home"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

   
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['home', 'name'], 
                name='unique device'
            )
        ]

class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)
    num_of_channels = models.IntegerField(choices=[(1, "1"),(2, "2"),(3, "3"), (4, "4")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Sensor(models.Model):
    """
    A sensor is a device that can be used to measure a certain thing.
    """
    owner = models.ForeignKey(to='account.User', on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=255)
    device = models.ForeignKey('mysite.Device',on_delete=models.CASCADE,null=True,related_name="sensors")
    topic_name = models.CharField(max_length=200,unique=True,blank=True,null=True)
    type = models.CharField(
        max_length=100,
        choices=[
            ("temperature", "Temperature"),
            ("humidity", "Humidity"),
            ("light", "Light"),
            ("motion", "Motion"),
        ],
        default="temperature",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def save(self,*args, **kwargs):
        self.topic_name = f"{self.device.home}{self.device.home.key}/{self.device}/{self.name}"
        return super().save()
    
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['device', 'name'], 
                name='unique sensor'
            )
        ]

class Sensor_cache(models.Model):
    state = models.CharField(max_length=200)
    sensor = models.ForeignKey('mysite.Sensor',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.state
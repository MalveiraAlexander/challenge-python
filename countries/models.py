from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=300, unique=True) 
    flag_img = models.URLField()
    capital_name = models.TextField(null=True) 
    population_count = models.BigIntegerField(null=True, blank=True) 
    continent_name = models.CharField(max_length=500) 
    all_timezone = models.TextField(null=True) 
    area = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name', 'id', 'continent_name']
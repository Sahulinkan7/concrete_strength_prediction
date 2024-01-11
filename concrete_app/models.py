from django.db import models

# Create your models here.

class Modelpredictions(models.Model):
    cement= models.DecimalField(decimal_places=7,max_digits=11)
    blast_furnace_slag = models.DecimalField(decimal_places=7,max_digits=11)
    fly_ash = models.DecimalField(decimal_places=7,max_digits=11)
    water = models.DecimalField(decimal_places=7,max_digits=11)
    superplasticizer = models.DecimalField(decimal_places=7,max_digits=11)
    coarse_aggregate = models.DecimalField(decimal_places=7,max_digits=11)
    fine_aggregate = models.DecimalField(decimal_places=7,max_digits=11)
    age = models.DecimalField(decimal_places=7,max_digits=11)
    concrete_compressive_strength = models.DecimalField(decimal_places=7,max_digits=11,blank=True,null=True)
    
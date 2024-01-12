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
    
class Modeltraining(models.Model):
    experiment_id = models.CharField(max_length = 100,null=True)
    running_status = models.CharField(max_length = 100,null=True)
    start_time = models.CharField(max_length = 100,null=True)
    stop_time = models.CharField(max_length = 100,null=True)
    execution_time = models.CharField(max_length = 100,null=True)
    message = models.CharField(max_length = 100,null=True)
    accuracy = models.CharField(max_length = 100,null=True)
    is_model_accepted = models.CharField(max_length = 100,null=True)
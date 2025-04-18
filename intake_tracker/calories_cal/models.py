from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class CaloriesIntake(models.Model):
    calories = models.FloatField(default=0.0)
    protein = models.FloatField(default=0.0)
    carbs = models.FloatField(default=0.0)  # Default to 0 liters
    fats=models.FloatField(default=0.0)
    fibers=models.FloatField(default=0.0)
    protein_goal=models.FloatField(default=120.0)
    carbs_goal=models.FloatField(default=0.00)
    fats_goal=models.FloatField(default=0.00)
    fibers_goal=models.FloatField(default=0.00)
 # Daily water intake goal, default 2 liters
    
class DietPlan(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly Active'),
        ('moderate', 'Moderately Active'),
        ('active', 'Very Active'),
        ('extra', 'Extra Active'),
    ]
    MEAL_CHOICES = [
        ('vegeterian','vegeterian'),
        ('non-vegeterian','non-vegeterian'),
        ('vegan','vegan'),
        ('vegeterian_nonvegeterian','vegeterian_nonvegeterian'),
       
        
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField(default=70)
    height = models.FloatField(default=171)
    age = models.IntegerField(default=28)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    meal_choice = models.CharField(max_length=25,choices=MEAL_CHOICES)
    activity_level = models.CharField(max_length=10, choices=ACTIVITY_CHOICES)

    # Calculated values
    calories = models.FloatField()
    proteins = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    fibers = models.FloatField()
    water = models.FloatField()

    def __str__(self):
        return f'Diet Plan for {self.user} ({self.calories} kcal)'



class Contact(models.Model):
    name=models.CharField(max_length=12)
    email=models.EmailField()
    phone=models.CharField(max_length=12)
    description=models.TextField()



    def __str__(self):
        
        return f"{self.name}  and  {self.email}  " 
    

